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

lut  = cdf.BiDirectionalLUT(atm.variables['VLEV'][:,0,0])
lin = cdf.BiDirectionalLinear(atm.variables['S_N_direction'][:])

plot1, axes1 = plt.subplots(1,2)
x = np.linspace(0,160,1000)
axes1[0].plot(x, lut.toOutputSpace(np.linspace(0,160,1000)))
x = np.linspace(0.005,3.95,1000)
axes1[1].plot(x, lut.toInputSpace(np.linspace(0.005,3.95,1000)))

plot1, axes1 = plt.subplots(1,2)
x = np.linspace(0,160,1000)
axes1[0].plot(x, lin.toOutputSpace(np.linspace(0,700,1000)))
x = np.linspace(0.005,3.95,1000)
axes1[1].plot(x, lin.toInputSpace(np.linspace(-1,5,1000)))

plt.show(block=False)
