#! /usr/bin/python3

import sys
sys.path.append('../')
from glob import glob

import xarray as xr
import numpy  as np

from netCDF4 import MFDataset

# mesonhFiles = '/home/pnarvor/work/nephelae/data/MesoNH-2019-02/REFHR.1.ARMCu.4D.nc'
# mesonhFiles = glob('/home/pnarvor/work/nephelae/data/nephelae-remote/Nephelae_tmp/download/L12zo.1.BOMEX.OUT.*.nc')
# mesonhFiles.sort()
mesonhFiles = '/home/pnarvor/work/nephelae/data/nephelae-remote/MesoNH02/bomex_hf.nc'
# mesonhFiles = ['/home/pnarvor/work/nephelae/data/nephelae-remote/MesoNH02/bomex_hf.nc']


atm0 = xr.open_mfdataset(mesonhFiles)
rct0  = atm0.RCT
# wind0 = {'ut':atm.UT, 'vt':atm.VT, 'wt':atm.WT}

# atm1 = MFDataset(mesonhFiles)
# rct1 = atm1.variables['RCT']



