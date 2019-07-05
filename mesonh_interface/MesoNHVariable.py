import numpy as np

from .NetCDFInterface   import NetCDFInterface
from .PeriodicContainer import PeriodicContainer
from .ScaledArray       import ScaledArray
from .DimensionHelper   import DimensionHelper

from nephelae_base.types import Position

class MesoNHVariable(ScaledArray):

    """MesoNHVariable

    Helper class to access MesoNH data using space coordinates
    instead of indexes.

    /!\ Reading is done using this order : [t,z,y,x]

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


    Member functions:
    
        
        __init__(atm, var, origin, interpolation):

            atm: (netCDF4.MFDataset) ALREADY OPENED to allow for several 
                 MesoNHVariables on the same MFDataset. (Is thread
                 protected by a mutex if only opened by MesoNHVariable types).
            
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

    tvar = 'time'
    zvar = 'VLEV'
    yvar = 'S_N_direction'
    xvar = 'W_E_direction'


    def __init__(self, atm, var, origin=None, interpolation='linear'):

        # Getting dimensions of MesoNH array and conversion in SI units
        tdim = atm.variables[MesoNHVariable.tvar][:]
        xdim = 1000.0*atm.variables[MesoNHVariable.xvar][:]
        ydim = 1000.0*atm.variables[MesoNHVariable.yvar][:]
        zdim = 1000.0*np.squeeze(atm.variables[MesoNHVariable.zvar][:,0,0])

        # Seems more logical to start a simulation at time 0.0 in any case ?
        tdim = tdim - tdim[0]
        
        # Reset origin if given
        if origin is not None:
            tdim = tdim - tdim[0] + origin[0]
            xdim = xdim - xdim[0] + origin[1]
            ydim = ydim - ydim[0] + origin[2]
            zdim = zdim - zdim[0] + origin[3]
        
        dimHelper = DimensionHelper()
        dimHelper.add_dimension(tdim, 'LUT')
        dimHelper.add_dimension(zdim, 'LUT')
        dimHelper.add_dimension(ydim, 'linear')
        dimHelper.add_dimension(xdim, 'linear')

        # Creating a ScaledArray with a PeriodicContainer as base
        # (MesoNH x,y are periodic)
        super().__init__(PeriodicContainer(NetCDFInterface(atm, var), [2,3]),
                         dimHelper, interpolation)
    

    # CANNOT DO THIS BECAUSE SUBARRAY INHERITS DIMENSIONNAL STRUCTURE
    # def __getitem__(self, keys):

    #     # Had to overload ScaledArray.__getitem__ because of
    #     # weird MesoNH [t,z,y,x] access

    #     """Access array data, key order is [t,x,y,z]
    #         Return a non-periodic scaled array, or
    #         a single floating point number.
    #     """
    #     
    #     return super().__getitem__((keys[0],keys[3],keys[2],keys[1]))


