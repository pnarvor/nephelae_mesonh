import numpy as np

from nephelae.types import Position, Bounds
from nephelae.array import DimensionHelper, PeriodicContainer, ScaledArray

from .MesonhInterface import MesonhInterface

class MesonhVariable(ScaledArray):

    """MesonhVariable

    Helper class to access MesoNH data using space coordinates
    instead of indexes.

    Attributes (inherited form mesonh_interface.ScaledArray):


        data (numpy like array): 

            Array holding the data. Is a instance of PeriodicContainer.
            (the last two dimensions are periodic).
            Defines self.__getitem__ and self.shape


        dimHelper (mesonh_interface.DimensionHelper):

            Helper class converting "unit" indices (in meters, seconds)
            in indexes to read in self.data.
       
        
        interpolation (string):

            Contains the interpolation type. (Can be nearest of linear).

        
        shape (tuple(int)): (Implemented in __getattr__)
            
            Getter to self.data.shape
        

        bounds (list(list(float))): (Implemented in __getattr__)

            NbDim x 2 nested list. First element of each nested list is the
            lowest bound of the dimension, and last element is the highest.
            (TODO define a specific type for this ?)
            
        
        span (list(float)): (Implemented in __getattr__)

            NbDim sized list holding the length of each dimension.


        actual_range (numpy array):

            Min and max of MesoNH variable.
            (wrapper around netCDF4.variables[var].actual_range)


    Member functions:
    
        
        __init__(atm, var, origin, interpolation):

            atm: (netCDF4.MFDataset) ALREADY OPENED to allow for several 
                 MesoNHVariables on the same MFDataset. (Is thread
                 protected by a mutex if only opened by MesonhVariable types).
            
            var: (string) Variable to read in the MFDataset.

            origin: (list(float)) Origin to give to the variable access.
                    /!\ (Event without specifying an origin, the time origin is 
                    always set to 0 regardless of the MFDataset time origin)

            interpolation: ('nearest' or 'linear') Specify the interpolation
                           type to use when reading the data.

        
        __getitem__([t,z,y,x]):
            
            Access the data using a tuple of floats or slice(float).
            /!\ x and y dimensions are periodic by default. The x and y
            parameters will accept any values.
            t,z,y,x can be either a float or a slice(float,float,None).

            /!\ There is not guaranty that the output bounds are exactly 
                the one given by a slice. The ouput bounds are the ones
                corresponding exaclty to the closest array elements.
                (underlying array is still discretized and each "pixel"
                has a fixed dimension "coordinate")
    """
    def __init__(self, atm, var, origin=None, interpolation='linear'):

        tdim = atm.dimensions[0]['data']
        xdim = atm.dimensions[3]['data']
        ydim = atm.dimensions[2]['data']
        zdim = atm.dimensions[1]['data']

        # Seems more logical to start a simulation at time 0.0 in any case ?
        tdim = tdim - tdim[0]
        
        # Reset origin if given
        if origin is not None:
            tdim = tdim - tdim[0] + origin[0]
            xdim = xdim - xdim[0] + origin[1]
            ydim = ydim - ydim[0] + origin[2]
            zdim = zdim - zdim[0] + origin[3]

        self.resolution = (
            (tdim[-1] - tdim[0]) / (len(tdim) - 1),
            (xdim[-1] - xdim[0]) / (len(xdim) - 1),
            (ydim[-1] - ydim[0]) / (len(ydim) - 1),
            (zdim[-1] - zdim[0]) / (len(zdim) - 1))

        
        dimHelper = DimensionHelper()
        # dimHelper.add_dimension(tdim, 'LUT')
        dimHelper.add_dimension(tdim, 'linear')
        dimHelper.add_dimension(xdim, 'linear')
        dimHelper.add_dimension(ydim, 'linear')
        dimHelper.add_dimension(zdim, 'LUT')

        # Creating a ScaledArray with a PeriodicContainer as base
        # (MesoNH x,y are periodic)
        super().__init__(PeriodicContainer(MesonhInterface(atm, var), [0,1,2]),
                         dimHelper, interpolation)

        actual_range = []
        for var in self.data.data.varData:
            if not hasattr(var, 'actual_range'):
                actual_range.append(Bounds())
            else:
                actual_range.append(var.actual_range)
        self.actual_range = tuple(actual_range)
    

    def __getitem__(self, keys):

        """
        /!\ This is essentially a wrapper around ScaledArray.__getitem__
        /!\ BUT WILL CROP THE KEYS TO FIT INTO THE ARRAY.
        """

        # not croping dim[2,3] because these dimensions are periodic in MesoNH
        return super().__getitem__(self.crop_keys(keys))


    def crop_keys(self, keys):

        """Crops keys to self.bounds"""

        # print("keys   :", keys)
        # print("bounds :", self.bounds)

        def crop_key(key, bounds):
            if isinstance(key, (int, float)):
                # If key is a single index not in bounds, always throw exception.
                if key < bounds.min or key > bounds.max:
                    raise IndexError("key " + str(key) + " is out of bounds ("
                                     + str(bounds) + ")")
                else:
                    return key
            elif isinstance(key, slice):
                # If key is a slice then crop slice into bounds if possible.
                # If not possible, throw exception.
                if key.start is None:
                    key_start = bounds.min
                else:
                    key_start = key.start

                if key.stop is None:
                    key_stop = bounds.max
                else:
                    key_stop = key.stop

                if key_stop < bounds.min or key_start > bounds.max:
                    raise IndexError("key " + str(key) + " is out of bounds ("
                                     + str(bounds) + ")")
                if key_start < bounds.min:
                    key_start = bounds.min
                if key_stop > bounds.max:
                    key_stop = bounds.max
                return slice(key_start, key_stop, None)
            else:
                raise ValueError("Index should be either a numeric type or a slice")
       
        # bounds = self.bounds
        # return (crop_key(keys[0], bounds[0]),
        #         keys[1], keys[2],
        #         crop_key(keys[3], bounds[3]))
        newKeys = []
        for key, b, periodic in zip(keys, self.bounds, self.data.isPeriodic):
            if periodic:
                newKeys.append(key)
            else:
                newKeys.append(crop_key(key, b))
        return tuple(newKeys)
