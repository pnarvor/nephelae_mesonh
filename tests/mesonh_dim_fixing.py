#! /usr/bin/python3

from xarray import open_mfdataset, open_dataset
import numpy as np
import matplotlib.pyplot as plt
import os

# root      = '/home/pnarvor/work/nephelae/data/nephelae-remote/MesoNH02/'
# inputFile = 'bomex_hf.nc'
root       = '/home/pnarvor/work/nephelae/data/MesoNH-2019-02/'
inputFile  = 'REFHR.1.ARMCu.4D.nc'
# inputFile  = 'REFHR.1.ARMCu.4D_fixed.nc'
# outputFile = 'REFHR.1.ARMCu.4D_fixed.nc'

atm = open_dataset(os.path.join(root, inputFile))

zData = np.array(atm.VLEV[:,0,0])

fig, axes = plt.subplots(1,1)
axes.plot(zData)
plt.show(block=False)

