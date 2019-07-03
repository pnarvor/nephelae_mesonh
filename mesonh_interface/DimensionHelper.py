import numpy as np
from scipy.interpolate import griddata
from scipy.interpolate import interp1d

class AffineTransform:
    
    def __init__(self, alpha, beta):
        self.alpha = alpha
        self.beta  = beta

    def __call__(self, x):
        return self.alpha * x + self.beta

class UnitsIndexConverter:

    """UnitsIndexConverter

    Base class to transform a tuple of index based indexing to a 
    tuple of units based indexing and vice-versa
    """

    def __init__(self, dimSize):
        self.dimSize = dimSize
    
    def to_unit(self, key):
        
        if isinstance(key, (int, float)):
            return float(self.toUnit(key))
        elif type(key) == slice:
            if key.start is None:
                key_start = self.to_unit(0)
            else:
                key_start = self.to_unit(key.start)
            if key.stop is None:
                key_stop = self.to_unit(self.dimSize - 1)  # -1 because python slice...
            else:
                key_stop = self.to_unit(key.stop - 1) # -1 because python slice...
            return slice(key_start, key_stop, None)
        raise ValueError("key must be a slice or a numeric type.")
    
    def to_index(self, key):
        
        if isinstance(key, (int, float)):
            return int(self.toIndex(key) + 0.5) # rounding to closest integer
        elif type(key) == slice:
            if key.start is None:
                key_start = 0
            else:
                key_start = int(self.to_index(key.start))
            if key.stop is None:
                key_stop = self.dimSize
            else:
                key_stop = self.to_index(key.stop) + 1 # +1 because python slice...
            return slice(key_start, key_stop, None)
        else:
            raise ValueError("key must be a slice or a numeric type.")

class AffineDimension(UnitsIndexConverter):

    """
    AffineDimension : maps input 1D indexes to output 1D scale through
                      affine transformation.
    """

    def __init__(self, dimSpan, dimSize):
        super().__init__(dimSize)

        self.toUnit  = AffineTransform((dimSpan[-1] - dimSpan[0]) / (self.dimSize - 1), dimSpan[0])
        self.toIndex = AffineTransform((self.dimSize - 1) / (dimSpan[-1] - dimSpan[0]),
                                       -dimSpan[0]*(self.dimSize - 1) / (dimSpan[-1] - dimSpan[0]))

class LookupTableDimension(UnitsIndexConverter):

    """
    LookupTableDimension : maps input 1D indexes to output 1D scale through an array
                           defining a stricly monotonous function.
    """

    def __init__(self, inputToOutput):
        super().__init__(len(inputToOutput))

        x_in = np.linspace(0, self.dimSize-1, len(inputToOutput))

        print(x_in)
        print(inputToOutput)
        
        # self.toUnit  = RegularGridInterpolator((x_in,), np.array(inputToOutput))
        # self.toIndex = RegularGridInterpolator((np.array(inputToOutput),), x_in)
        self.toUnit  = interp1d(x_in, np.array(inputToOutput))
        self.toIndex = interp1d(np.array(inputToOutput), x_in)

class DimensionHelper:

    """DimensionHelper
    Helper class to convert a tuple of indexes or units to
    their units or indexes counterpart. To be used in ScaledArray
    """

    def __init__(self):
       self.dims = []

    def add_dimension(self, params, typ='affine', dimLen=None):
        if typ == 'affine':
            if dimLen is None:
                dimLen = len(params)
            self.dims.append(AffineDimension([params[0], params[-1]], dimLen))
        elif typ == 'LUT':
            self.dims.append(LookupTableDimension(params))
        else:
            raise ValueError("Invalid dimension type '" + typ + "'")

    def to_unit(self, keys):

        if not isinstance(keys, (tuple, list)):
            keys = (keys,)
        
        if len(keys) != len(self.dims):
            raise ValueError("Number or keys must be equal to number of " +
                             "Dimension (" + str(len(keys)) + "/" + 
                             str(len(self.dims)) + ")")
        res = []
        for key, dim in zip(keys, self.dims):
            res.append(dim.to_unit(key))
        return tuple(res)

    def to_index(self, keys):
        
        if not isinstance(keys, (tuple, list)):
            keys = (keys,)
        
        if len(keys) != len(self.dims):
            raise ValueError("Number or keys must be equal to number of " +
                             "Dimension (" + str(len(keys)) + "/" + 
                             str(len(self.dims)) + ")")
        res = []
        for key, dim in zip(keys, self.dims):
            res.append(dim.to_index(key))
        return tuple(res)


