#! /usr/bin/python3

import os
import time
import numpy as np
import math as m
import matplotlib.pyplot as plt
from   matplotlib import animation

from netCDF4 import MFDataset

from nephelae_simulation.mesonh_interface import ScaledArray
from nephelae_simulation.mesonh_interface import DimensionHelper
from nephelae_simulation.mesonh_interface import MesoNHVariable

var0 = 'RCT'
# var1 = 'UT'     # WE wind
# var1 = 'VT'     # SN wind
var1 = 'WT'     # vertical wind
# var1 = 'TKET'   # Turbulent kinetic energy
# var1 = 'PABST'  # Absolute pressure
# var1 = 'RVT'    # Vapor mixing ratio
# var1 = 'RRT'    # Rain mixing ratio
# var1 = 'SVT001' # User data (?)
# var1 = 'SVT002' # User data (?)
# var1 = 'SVT003'  # User data (?)

atm = MFDataset('/home/pnarvor/work/nephelae/data/MesoNH-2019-02/REFHR.1.ARMCu.4D.nc')

tvar = atm.variables['time'][:]
tvar = tvar - tvar[0]
xvar = 1000.0*atm.variables['W_E_direction'][:]
yvar = 1000.0*atm.variables['S_N_direction'][:]
zvar = 1000.0*np.squeeze(atm.variables['VLEV'][:,0,0])

atmShape = type('AtmShape', (), {})()
atmShape.t = len(tvar)
atmShape.z = len(zvar)
atmShape.x = len(xvar)
atmShape.y = len(yvar)

print("Shape : (", atmShape.t, atmShape.z, atmShape.x, atmShape.y, ")")

# data0 = MesoNHVariable(atm, var0, interpolation='nearest')
# data1 = MesoNHVariable(atm, var1, interpolation='nearest')
data0 = MesoNHVariable(atm, var0, interpolation='linear')
data1 = MesoNHVariable(atm, var1, interpolation='linear')

z0 = 1100.0
y0 = 4500.0
xySlice = slice(0.0, 12000.0, None)
tStart = time.time()

xyBounds = data0[0.0,z0,xySlice,xySlice].bounds
xyExtent = [xyBounds[0][0], xyBounds[0][1], xyBounds[1][0], xyBounds[1][1]]
xzBounds = data0[0.0,:,xySlice,y0].bounds
xzExtent = [xzBounds[1][0], xzBounds[1][1], xzBounds[0][0], xzBounds[0][1]]

print('Started !')

fig, axes = plt.subplots(2,2, sharex=True)
varDisp0 = axes[0][0].imshow(data0[0.0, z0, xySlice, xySlice].data, cmap=plt.cm.viridis, origin='lower', extent=xyExtent)
varDisp1 = axes[1][0].imshow(data0[0.0,  :,      y0, xySlice].data, cmap=plt.cm.viridis, origin='lower', extent=xzExtent)
varDisp2 = axes[0][1].imshow(data1[0.0, z0, xySlice, xySlice].data, cmap=plt.cm.viridis, origin='lower', extent=xyExtent)
varDisp3 = axes[1][1].imshow(data1[0.0,  :,      y0, xySlice].data, cmap=plt.cm.viridis, origin='lower', extent=xzExtent)

def init():

    axes[0][0].plot([xySlice.start, xySlice.stop], [y0, y0], color=[0.0,0.0,0.0,1.0])
    axes[1][0].plot([xySlice.start, xySlice.stop], [z0, z0], color=[0.0,0.0,0.0,1.0])
    axes[0][1].plot([xySlice.start, xySlice.stop], [y0, y0], color=[0.0,0.0,0.0,1.0])
    axes[1][1].plot([xySlice.start, xySlice.stop], [z0, z0], color=[0.0,0.0,0.0,1.0])

def update(i):
    
    fastForward = 20.0
    t = fastForward*(time.time() - tStart)
    t = t - int(t / (tvar[-1] - tvar[0]))*(tvar[-1] - tvar[0])

    varDisp0.set_data(data0[t, z0, xySlice, xySlice].data)
    varDisp1.set_data(data0[t,  :,      y0, xySlice].data)
    varDisp2.set_data(data1[t, z0, xySlice, xySlice].data)
    varDisp3.set_data(data1[t,  :,      y0, xySlice].data)

    # time.sleep(0.1)

anim = animation.FuncAnimation(
    fig,
    update,
    init_func=init,
    frames=atmShape.x*atmShape.y,
    interval = 1)

plt.show(block=False)



