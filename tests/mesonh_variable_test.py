#! /usr/bin/python3

import sys
sys.path.append('../')
from netCDF4 import MFDataset
import numpy as np
import matplotlib.pyplot as plt

from mesonh_probe import MesoNHVariable

atm = MFDataset('/home/pnarvor/work/nephelae/data/MesoNH-2019-02/REFHR.1.ARMCu.4D.nc')
var = MesoNHVariable(atm, 'RCT')

fig, axes = plt.subplots(1,1)
axes.imshow(np.squeeze(var[0,45,0:512,0:512]))





