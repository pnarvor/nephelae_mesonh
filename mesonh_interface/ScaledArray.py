

class ScaledArray:

    """ScaledArray

    Helper class for accessing an array of which indexes are bound to
    a continous scale (for example a array a samples in space on which
    dimensions are in meters)

    Attributes:
    
    data                      (numpy-like array): Regular numpy-like array which holds the data
    dimHelper (mesonh_interface.DimensionHelper): Helper type which transform floating points
                                                  keys into index keys to read into the data.

    """

    def __init__(self, data, dimHelper=None):

        self.data     = data
        self.dimHelper = dimHelper


    def __getattr__(self, name):

        if name == 'shape':
            return self.data.shape
        raise ValueError("ScaledArray has no attribute '"+name+"'")


    def __getitem__(self, keys):

        return self.data[self.dimHelper.to_index(keys)]


