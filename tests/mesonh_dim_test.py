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



# dims = cdf.MesoNHDimensionHelper(atm)
# print(dims.to_units(cdf.Fancy()[1,0:161,0:400,0:400]))
# print(dims.to_units(cdf.Fancy()[0:144,0:161,0:400,0:400]))
# print(dims.to_units(cdf.Fancy()[0:144,0:161,0:750,0:750]))
# print(dims.to_indexes(cdf.Fancy()[77999512,0.5:2.5,-2.5:7.5,0.5:2.5]))
