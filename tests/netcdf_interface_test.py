#! /usr/bin/python3

import sys
sys.path.append('../')

import numpy as np
from netCDF4 import MFDataset
import netcdf_probe as cdf


mesonhFiles = sys.argv[slice(1,len(sys.argv))]
atm = MFDataset(mesonhFiles)

# netcdf = cdf.NetCDFInterface(atm, 'RCT', periodicVariables=['S_N_direction'])
netcdf = cdf.NetCDFInterface(atm, 'RCT', periodicVariables=['S_N_direction', 'W_E_direction'])

# array = netcdf[26,160,400,500:200]
netcdf[26,160,10:500,200:1200]
# netcdf[26,160,480,-1:60]
# print("Shape : ", array.shape)


# array = np.array([[1,2],[3,4]])
# print(array)
# print(array.shape)
# print(tuple([2,2]))

