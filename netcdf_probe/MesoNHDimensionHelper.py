import numpy as np

from .BiDirectionalLUT    import BiDirectionalLUT
from .BiDirectionalLinear import BiDirectionalLinear

def clip_key(key, dimLen):
    if isinstance(key, slice):
        if key.start < 0:
            key_start = 0
        elif key.start > dimLen:
            key_start = dimLen
        else:
            key_start = key.start
        if key.stop < 0:
            key_stop = 0
        elif key.stop > dimLen:
            key_stop = dimLen
        else:
            key_stop = key.stop
        return slice(int(key_start), int(key_stop), None)
    else:
        if key < 0:
            return 0
        elif key >= dimLen:
            return dimLen - 1
        else:
            return int(key)

def clip_unit(key, unitMin, unitMax):
    if isinstance(key, slice):
        if key.start < unitMin:
            key_start = unitMin
        elif key.start > unitMax:
            key_start = unitMax
        else:
            key_start = key.start
        if key.stop < unitMin:
            key_stop = unitMin
        elif key.stop > unitMax:
            key_stop = unitMax
        else:
            key_stop = key.stop
        return slice(key_start, key_stop, key.step)
    else:
        if key < unitMin:
            return unitMin
        elif key >= unitMax:
            return unitMax
        else:
            return key

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
        self.__atm = atm
        t_arr = atm.variables[MesoNHDimensionHelper.t_name][:]
        z_arr = atm.variables[MesoNHDimensionHelper.z_name][:,0,0]
        x_arr = atm.variables[MesoNHDimensionHelper.x_name][:]
        y_arr = atm.variables[MesoNHDimensionHelper.y_name][:]

        self.atmShape = (len(t_arr), len(z_arr), len(x_arr), len(y_arr),)
        self.atmSpan  = (slice(t_arr[0], t_arr[-1]),
                         slice(z_arr[0], z_arr[-1]),
                         slice(x_arr[0], x_arr[-1]),
                         slice(y_arr[0], t_arr[-1]),)
        
        self.converter_t = BiDirectionalLUT(t_arr)
        self.converter_z = BiDirectionalLUT(z_arr)
        self.converter_x = BiDirectionalLinear(x_arr)
        self.converter_y = BiDirectionalLinear(y_arr)

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
            return float(self.converter_t.to_output_space([key]))

    def to_index_t(self, key):
        if isinstance(key, slice):
            tmp = np.floor(self.converter_t.to_input_space([key.start, key.stop])).astype(int)
            return slice(tmp[0], tmp[1] + 1, None)
        else:
            return float(self.converter_t.to_input_space([key]))
        
    def to_unit_z(self, key):
        if isinstance(key, slice):
            tmp = self.converter_z.to_output_space([key.start, key.stop - 1])
            return slice(tmp[0], tmp[1], None)
        else:
            return float(self.converter_z.to_output_space([key]))

    def to_index_z(self, key):
        if isinstance(key, slice):
            tmp = np.floor(self.converter_z.to_input_space([key.start, key.stop])).astype(int)
            return slice(tmp[0], tmp[1] + 1, None)
        else:
            return float(self.converter_z.to_input_space([key]))
        
    def to_unit_x(self, key):
        if isinstance(key, slice):
            tmp = self.converter_x.to_output_space([key.start, key.stop - 1])
            return slice(tmp[0], tmp[1], None)
        else:
            return float(self.converter_x.to_output_space([key]))

    def to_index_x(self, key):
        if isinstance(key, slice):
            tmp = np.floor(self.converter_x.to_input_space([key.start, key.stop])).astype(int)
            return slice(tmp[0], tmp[1] + 1, None)
        else:
            return float(self.converter_x.to_input_space([key]))
        
    def to_unit_y(self, key):
        if isinstance(key, slice):
            tmp = self.converter_y.to_output_space([key.start, key.stop - 1])
            return slice(tmp[0], tmp[1], None)
        else:
            return float(self.converter_y.to_output_space([key]))

    def to_index_y(self, key):
        if isinstance(key, slice):
            tmp = np.floor(self.converter_y.to_input_space([key.start, key.stop])).astype(int)
            return slice(tmp[0], tmp[1] + 1, None)
        else:
            return float(self.converter_y.to_input_space([key]))

    def clip_keys(self, keys):
        # keys 2 and 3 are not clipped due to periodicity of x.y dims
        res = (clip_key(keys[0], self.atmShape[0]),
               clip_key(keys[1], self.atmShape[1]),)
        if isinstance(keys[2], slice):
            res = res + (slice(int(keys[2].start), int(keys[2].stop), None),)
        else:
            res = res + (int(keys[2]),)
        if isinstance(keys[3], slice):
            res = res + (slice(int(keys[3].start), int(keys[3].stop), None),)
        else:
            res = res + (int(keys[3]),)
        return res

    def clip_units(self, keys):
        # keys 2 and 3 are not clipped due to periodicity of x,y dims
        res = (clip_unit(keys[0], self.atmSpan[0].start, self.atmSpan[0].stop),
               clip_unit(keys[1], self.atmSpan[1].start, self.atmSpan[1].stop),
               keys[2], keys[3],)
        return res



