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

dims = cdf.MesoNHDimensionHelper(atm)
print(dims[10.0,2.0,0.005,2.0])


