import numpy as np
from scipy.interpolate import griddata
from scipy.interpolate import RegularGridInterpolator

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
        
        if isinstance(key, (int, long, float)):
            return self.toUnit(key)
        elif type(key) == slice:
            if key[0] is None:
                key_start = self.toUnit(0)
            else:
                key_start = self.to_unit(key[0])
            if key[1] is None:
                key_stop = self.toUnit(self.N - 1)  # -1 because python slice...
            else:
                key_stop = self.to_unit(key[1] - 1) # -1 because python slice...
            return slice(key_start, key_stop, None)
        raise ValueError("key must be a slice or a numeric type.")
    
    def to_index(self, key):
        
        if isinstance(key, (int, long, float)):
            return int(self.toIndex(key) + 0.5) # rounding to closest integer
        elif type(key) == slice:
            if key[0] is None:
                key_start = 0
            else:
                key_start = int(self.to_index(key[0]))
            if key[1] is None:
                key_stop = self.N
            else:
                key_stop = self.to_index(key[1]) + 1 # +1 because python slice...
            return slice(key_start, key_stop, None)
        else:
            raise ValueError("key must be a slice or a numeric type.")

class LookupTableDimension(UnitsIndexConverter):

    """
    LookupTableDimension : maps input 1D indexes to output 1D scale through an array
                           defining a stricly monotonous function.
    """

    def __init__(self, inputToOutput):
        super().__init__(len(inputToOutput))

        x_in = np.linspace(0, self.N-1, len(inputToOutput))
        
        self.toUnit  = RegularGridInterpolator((x_in,), inputToOutput)
        self.toIndex = RegularGridInterpolator((inputToOutput,), x_in)

class AffineDimension(UnitsIndexConverter):

    """
    AffineDimension : maps input 1D indexes to output 1D scale through
                      affine transformation.
    """

    def __init__(self, dimSpan, dimSize):

        self.N = dimSize
        self.toUnit  = AffineTransform((dimSpan[-1] - dimSpan[0]) / (self.N - 1), dimSpan[0])
        self.toIndex = AffineTransform((self.N - 1) / (dimSpan[-1] - dimSpan[0]),
                                       -dimSpan[0]*self.toIndexAlpha)

class DimensionHelper:

    def __init__(self, dimensions):

       self.dims = dimensions

