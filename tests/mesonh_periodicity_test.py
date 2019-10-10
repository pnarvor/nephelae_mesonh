#! /usr/bin/python3

import os
import time
import numpy as np
import math as m
import matplotlib.pyplot as plt
from   matplotlib import animation

from xarray import open_mfdataset

# mesonhFiles = '/home/pnarvor/work/nephelae/data/MesoNH-2019-02/REFHR.1.ARMCu.4D.nc'
# mesonhFiles = '/home/pnarvor/work/nephelae/data/nephelae-remote/MesoNH02/bomex_hf.nc'
mesonhFiles = '/home/pnarvor/work/nephelae/data/skyscanner-remote/Nephelae/MesoNH-2019-10/L12zo.1.BOMEX.OUT.040.nc'

atm = open_mfdataset(mesonhFiles)
wt  = atm.WT
print("Shape :", wt.shape)

# t0 = 40
t0 = 0
z0 = 40

borderSize = 10
snBorders  = np.empty([wt.shape[2], 2*borderSize])
snBorders[:, :borderSize] = wt[t0,z0,:,-borderSize:]
snBorders[:,-borderSize:] = wt[t0,z0,:, :borderSize]

toRemove = 6
wt0 = wt[t0,z0,:,:-toRemove]
snBorders0  = np.empty([wt0.shape[0], 2*borderSize])
snBorders0[:, :borderSize] = wt0[:,-borderSize:]
snBorders0[:,-borderSize:] = wt0[:, :borderSize]

pad = 0
bottom = np.array(wt[t0,z0,:,:(toRemove + pad)]).squeeze()
top    = np.array(wt[t0,z0,:,-(toRemove + pad):]).squeeze()
diff0   = top - bottom
print("Residual top/bottom:", np.linalg.norm(diff0.ravel()))

pad = 0
left  = np.array(wt[t0,z0,:(toRemove + pad) ,:]).squeeze()
right = np.array(wt[t0,z0,-(toRemove + pad):,:]).squeeze()
diff1 = right - left
print("Residual right/left:", np.linalg.norm(diff1.ravel()))

fig, axes = plt.subplots(3,1, sharex=True)
axes[0].imshow(np.array(wt[t0,z0,:,:].data).squeeze().T, origin='lower')
axes[1].imshow( snBorders.T, origin='lower')
axes[2].imshow(snBorders0.T, origin='lower')

fig, axes = plt.subplots(3,1, sharex=True)
axes[0].set_title("Bottom/Top")
axes[0].imshow(bottom.T, origin='lower')
axes[1].imshow(   top.T, origin='lower')
axes[2].imshow( diff0.T, origin='lower')

fig, axes = plt.subplots(3,1, sharex=True)
axes[0].set_title("Left/Right")
axes[0].imshow( left, origin='lower')
axes[1].imshow(right, origin='lower')
axes[2].imshow(diff1, origin='lower')


plt.show(block=False)




