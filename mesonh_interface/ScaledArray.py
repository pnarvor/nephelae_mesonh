

class ScaledArray:

    """ScaledArray

    Helper class for accessing an array of which indexes are bound to
    a continous scale (for example a array a samples in space on which
    dimensions are in meters)

    """

    def __init__(self, array, dimHelper=None):

        self.array     = array
        self.dimHelper = dimHelper

    def __getattr__(self, name):
        if name == 'shape':
            return self.array.shape
        raise ValueError("ScaledArray has no attribute '"+name+"'")
