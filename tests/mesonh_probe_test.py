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
print("MesoNH loaded !")

probe = cdf.MesoNHProbe(atm, ['RCT','WT'])

position = cdf.Fancy()[probe.t0,0.01,0,0]
# v = 0.025
v = 0.020
# dt = 1.0
dt = 0.1

probe.update_cache(position, blocking=True)

for i in range(1000):
    print(position, " : ", probe[position])
    # newPos = ()
    # for p in position:
    #     newPos = newPos + (p + v * dt,)
    # position = newPos
    position = (position[0] + dt,
                position[1],
                position[2],
                position[3] + v*dt,)
    time.sleep(dt)

# # cache = cdf.MultiCache([cdf.MesoNHVariable(atm, 'RCT'), cdf.MesoNHVariable(atm, 'WT')])
# cache = probe.getCache()
# cache.load(cdf.Fancy()[10,0:160,128,0:300], blocking=True)
# 
# image0 = np.flip(np.squeeze(cache.buffers[0]), 0)
# image1 = np.flip(np.squeeze(cache.buffers[1]), 0)
# 
# # plt.imshow(image0, cmap='viridis')
# plt.imshow(image1, cmap='viridis')
# plt.show(block=False)



