#! /usr/bin/python3

import sys
import os
sys.path.append('../')
import numpy as np
import matplotlib.pyplot as plt
import imageio
import matplotlib.cm as cm
import time

from netCDF4 import MFDataset
import netcdf_probe as cdf

"""
test file for periodiccontainer and netcdfinterface types
    - arguments : mesonh (netcdf) files to open
"""

mesonhfiles = sys.argv[slice(1,len(sys.argv))]
atm = MFDataset(mesonhfiles)

probe = cdf.MesoNHProbe(atm, ['RCT', 'THT'], [10,20,20,20], initPosition=[10,20,20,20])
# probe = cdf.MesoNHProbe(atm, ['RCT'], [10,20,20,20], initPosition=[10,20,20,20])

for i in range(30):
    # print(probe[10,20,20,20 + i],"\n\n\n")
    print(probe[10,20,20,20 + i],"\n")
    time.sleep(0.5)



