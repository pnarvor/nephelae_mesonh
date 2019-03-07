import numpy as np

from .BiDirectionalLUT    import BiDirectionalLUT
from .BiDirectionalLinear import BiDirectionalLinear

class MesoNHDimensionHelper:

    """
    MesoNHDimensionHelper : helper to convert values and slices
                            from array index values to mesonh units
                            and vice versa
    """

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
        # index/units converters
        self.converter_t = BiDirectionalLUT(atm.variables[MesoNHDimensionHelper.t_name][:])
        self.converter_z = BiDirectionalLUT(atm.variables[MesoNHDimensionHelper.z_name][:,0,0])
        self.converter_x = BiDirectionalLinear(atm.variables[MesoNHDimensionHelper.x_name][:])
        self.converter_y = BiDirectionalLinear(atm.variables[MesoNHDimensionHelper.y_name][:])

    def to_units(self, keys):
        return (self.to_unit_t(keys[0]),
                self.to_unit_z(keys[1]),
                self.to_unit_x(keys[2]),
                self.to_unit_y(keys[3]))

    def to_indexes(self, keys):
        return (self.to_index_t(keys[0]),
                self.to_index_z(keys[1]),
                self.to_index_x(keys[2]),
                self.to_index_y(keys[3]))

    def to_unit_t(self, key):
        if isinstance(key, slice):
            tmp = self.converter_t.to_output_space([key.start, key.stop - 1])
            return slice(tmp[0], tmp[1], None)
        else:
            return self.converter_t.to_output_space(key)

    def to_index_t(self, key):
        if isinstance(key, slice):
            tmp = np.floor(self.converter_t.to_input_space([key.start, key.stop])).astype(int)
            return slice(tmp[0], tmp[1] + 1, None)
        else:
            return self.converter_t.to_input_space(key)
        
    def to_unit_z(self, key):
        if isinstance(key, slice):
            tmp = self.converter_z.to_output_space([key.start, key.stop - 1])
            return slice(tmp[0], tmp[1], None)
        else:
            return self.converter_z.to_output_space(key)

    def to_index_z(self, key):
        if isinstance(key, slice):
            tmp = np.floor(self.converter_z.to_input_space([key.start, key.stop])).astype(int)
            return slice(tmp[0], tmp[1] + 1, None)
        else:
            return self.converter_z.to_input_space(key)
        
    def to_unit_x(self, key):
        if isinstance(key, slice):
            tmp = self.converter_x.to_output_space([key.start, key.stop - 1])
            return slice(tmp[0], tmp[1], None)
        else:
            return self.converter_x.to_output_space(key)

    def to_index_x(self, key):
        if isinstance(key, slice):
            tmp = np.floor(self.converter_x.to_input_space([key.start, key.stop])).astype(int)
            return slice(tmp[0], tmp[1] + 1, None)
        else:
            return self.converter_x.to_input_space(key)
        
    def to_unit_y(self, key):
        if isinstance(key, slice):
            tmp = self.converter_y.to_output_space([key.start, key.stop - 1])
            return slice(tmp[0], tmp[1], None)
        else:
            return self.converter_y.to_output_space(key)

    def to_index_y(self, key):
        if isinstance(key, slice):
            tmp = np.floor(self.converter_y.to_input_space([key.start, key.stop])).astype(int)
            return slice(tmp[0], tmp[1] + 1, None)
        else:
            return self.converter_y.to_input_space(key)
        

        
