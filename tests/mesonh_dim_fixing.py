#! /usr/bin/python3

from xarray import open_mfdataset
import numpy as np
import matplotlib.pyplot as plt
import os

# mesonhFiles = '/home/pnarvor/work/nephelae/data/MesoNH-2019-02/REFHR.1.ARMCu.4D.nc'
root       = '/home/pnarvor/work/nephelae/data/MesoNH-2019-02/'
inputFile  = 'REFHR.1.ARMCu.4D.nc'
outputFile = 'REFHR.1.ARMCu.4D_fixed.nc'

atm = open_mfdataset(os.path.join(root, inputFile))

zData = np.array(atm.VLEV[:,0,0])

cmd = "ncap2 -s 'vertical_levels(:)={'" 
for z in zData:
    cmd = cmd + str(z) + ","
cmd = cmd + "}' " + os.path.join(root, inputFile) + " " + os.path.join(root, outputFile)
print(cmd)

# fig, axes = plt.subplots(1,1)
# axes.plot(zData)
# plt.show(block=False)

