import numpy as np

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
        # Dimension arrays
        self.dim_t = np.array(atm.variables[MesoNHDimensionHelper.t_name][:])
        self.dim_z = np.array(atm.variables[MesoNHDimensionHelper.z_name][:,0,0])
        self.dim_x = np.array(atm.variables[MesoNHDimensionHelper.x_name][:])
        self.dim_y = np.array(atm.variables[MesoNHDimensionHelper.y_name][:])


        

        
