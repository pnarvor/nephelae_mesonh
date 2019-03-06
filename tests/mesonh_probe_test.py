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

probe = cdf.MesoNHProbe(atm, ['RCT','WT'])
# cache = cdf.MultiCache([cdf.MesoNHVariable(atm, 'RCT'), cdf.MesoNHVariable(atm, 'WT')])
cache = probe.getCache()
cache.load(cdf.Fancy()[10,0:160,128,0:300], blocking=True)

image0 = np.flip(np.squeeze(cache.buffers[0]), 0)
image1 = np.flip(np.squeeze(cache.buffers[1]), 0)

# plt.imshow(image0, cmap='viridis')
plt.imshow(image1, cmap='viridis')
plt.show(block=False)



