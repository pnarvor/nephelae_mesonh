#! /usr/bin/python3

import sys
import os
sys.path.append('../')
import numpy as np
import matplotlib.pyplot as plt
import imageio
import matplotlib.cm as cm

from netCDF4 import MFDataset
import mesonh_probe as cdf

"""
Test file for PeriodicContainer and NetCDFInterface types
    - Arguments : MesoNH (netcdf) files to open
"""

mesonhFiles = sys.argv[slice(1,len(sys.argv))]
atm = MFDataset(mesonhFiles)
print('MesoNH opened')

data = cdf.DoubleBufferedCache(cdf.PeriodicContainer(cdf.NetCDFInterface(atm, 'RCT'), [2,3]))

data.load(cdf.Fancy()[0,0,0:800,0:800], blocking=True)
print("Coucou !")




