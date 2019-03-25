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
import mesonh_probe as cdf

"""
test file for periodiccontainer and netcdfinterface types
    - arguments : mesonh (netcdf) files to open
"""

mesonhfiles = sys.argv[slice(1,len(sys.argv))]
atm = MFDataset(mesonhfiles)
print("MesoNH loaded !")

# probe = cdf.MesoNHProbe(atm, ['RCT'])
# probe = cdf.MesoNHProbe(atm, ['WT'])
probe = cdf.MesoNHProbe(atm, ['RCT','WT'])
# probe = cdf.MesoNHProbe(atm, ['RCT','UT','VT','WT'])
# probe = cdf.MesoNHProbe(atm, ['UT','VT'])

# probe._MesoNHProbe__targetCacheSpan = cdf.Fancy()[30, -0.3:0.3, -0.6:0.6, -0.6:0.6]
probe._MesoNHProbe__targetCacheSpan = cdf.Fancy()[10, -0.2:0.1, -0.2:0.2, -0.2:0.2]
probe._MesoNHProbe__updateThreshold = 0.0
# probe._MesoNHProbe__updateThreshold = 0.1

position = cdf.Fancy()[probe.t0 + 2000, 2.0, 0.0, 0.0]
# v = 0.025
v = 0.020
dt = 1.0
# dt = 0.1

probe.update_cache(position, blocking=True)

for i in range(1000):
    print("Read ", i, " : ", position, ", ", probe[position])
    # tmp = probe[position]
    position = (position[0] + dt,
                position[1],
                position[2],
                position[3] + v*dt,)
    time.sleep(dt)
    # time.sleep(2*dt)
    # time.sleep(0.5*dt)
    # time.sleep(1.0)




