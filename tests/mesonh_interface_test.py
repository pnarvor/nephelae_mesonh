#! /usr/bin/python3

import sys
sys.path.append('../')
# from netCDF4 import MFDataset

from nephelae_mesonh import MesonhInterface, MesonhDataset

# mesonhFiles = '/home/pnarvor/work/nephelae/data/MesoNH-2019-02/REFHR.1.ARMCu.4D.nc'
mesonhFiles = '/home/pnarvor/work/nephelae/data/nephelae-remote/Nephelae_tmp/download/L12zo.1.BOMEX.OUT.*.nc'

atm = MesonhDataset(mesonhFiles)
var = MesonhInterface(atm, ['RCT','WT'])

a0 = var[0,0,:,:]
a1 = var[1,1,:,:]
a2 = a1 + a0

print(a2.shape)

