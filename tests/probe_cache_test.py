#! /usr/bin/python3

import sys
import os
sys.path.append('../')
import numpy as np
import matplotlib.pyplot as plt
import imageio
import matplotlib.cm as cm

from netCDF4 import MFDataset
import netcdf_probe as cdf
import time

"""
Test file for PeriodicContainer and NetCDFInterface types
    - Arguments : MesoNH (netcdf) files to open
"""

mesonhFiles = sys.argv[slice(1,len(sys.argv))]
atm = MFDataset(mesonhFiles)
print('MesoNH opened')



data = cdf.ProbeCache(cdf.PeriodicContainer(cdf.NetCDFInterface(atm, 'RCT'), [2,3]), (20,30,30,30), initPosition=[10,50,200,200])
# data.update_cache([10,50,100,100], blocking=True)

time.sleep(1)

# i = 0
# print(data[10, 50, 200:203, (200 + 3*i):(203 + 3*i)])

for i in range(35):
#     print((data[10, 50, 200:203, (200 + 3*i):(203 + 3*i)]).shape)
    print(data[10 + i, 50, 200:203, (200 + 3*i):(203 + 3*i)])
    time.sleep(0.2)




