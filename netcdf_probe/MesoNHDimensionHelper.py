import numpy as np

class DimensionLookUpTable:

    "Used for non periodic index conversion"

    def __init__(self, dimValues, linear=False):

        self.linear = linear
        self.min    = np.min(dimValues)
        self.max    = np.max(dimValues)
        self.factor = len(dimValues - 1) / (self.max - self.min)

        x_values = np.linspace(self.min, self.max, len(dimValues))
        self.lut = np.searchsorted(dimValues, x_values, 'right')

    def __getitem__(self, key):
        if self.linear:
            return int(self.factor * (key - self.min))
        else:
            return self.lut[int(self.factor * (key - self.min))]

class MesoNHDimensionHelper:

    # Have to define dimension varaibles hard because dim_z != var_z in MesoNH files
    # also assuming units = km
    t_name = 'time'
    z_name = 'VLEV'
    x_name = 'W_E_direction'
    y_name = 'S_N_direction'

    def __init__(self, atm):

        """
        - atm         : MFDataset from netCDF4 package ALREADY LOADED with
                        a set of mesonh files
        """
        # Dimension arrays
        self.dim_t = np.array(atm.variables[MesoNHDimensionHelper.t_name][:])
        self.dim_z = np.array(atm.variables[MesoNHDimensionHelper.z_name][:,0,0])
        self.dim_x = np.array(atm.variables[MesoNHDimensionHelper.x_name][:])
        self.dim_y = np.array(atm.variables[MesoNHDimensionHelper.y_name][:])

        self.dim_t = self.dim_t - self.dim_t[0]
        self.luts = [DimensionLookUpTable(self.dim_t, linear=False), \
                     DimensionLookUpTable(self.dim_z, linear=False), \
                     DimensionLookUpTable(self.dim_x, linear=True),  \
                     DimensionLookUpTable(self.dim_y, linear=True)]

    def __getitem__(self, keys):

        """
        return slices of length 2 to be used to
        get an array on which make a linear interpolation
        """

        res = ()
        for key, lut in zip(keys, self.luts):
            if isinstance(key, slice):
                raise Exception("MesoNHDimensionHelder cannot yet handle slices")
            tmp = lut[key]
            res = res + (slice(tmp, tmp + 1, None),)
        return res
        

        
