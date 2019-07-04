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

dimHelper = DimensionHelper()
dimHelper.add_dimension(tvar, 'LUT')
dimHelper.add_dimension(zvar, 'LUT')
dimHelper.add_dimension(xvar, 'linear')
dimHelper.add_dimension(yvar, 'linear')

# data0 = ScaledArray(atm.variables[var0], dimHelper, interpolation='nearest')
# data1 = ScaledArray(atm.variables[var1], dimHelper, interpolation='nearest')
data0 = ScaledArray(atm.variables[var0], dimHelper, interpolation='linear')
data1 = ScaledArray(atm.variables[var1], dimHelper, interpolation='linear')

z0 = 1100.0
y0 = 4500.0
tStart = time.time()

print('Started !')

fig, axes = plt.subplots(2,2, sharex=True)
varDisp0 = axes[0][0].imshow(data0[0.0,z0,:,:].data, cmap=plt.cm.viridis, origin='lower', extent=[xvar[0],xvar[-1],yvar[0],yvar[-1]])
varDisp1 = axes[1][0].imshow(data0[0.0,:,y0,:].data, cmap=plt.cm.viridis, origin='lower', extent=[xvar[0],xvar[-1],zvar[0],zvar[-1]])
varDisp2 = axes[0][1].imshow(data1[0.0,z0,:,:].data, cmap=plt.cm.viridis, origin='lower', extent=[xvar[0],xvar[-1],yvar[0],yvar[-1]])
varDisp3 = axes[1][1].imshow(data1[0.0,:,y0,:].data, cmap=plt.cm.viridis, origin='lower', extent=[xvar[0],xvar[-1],zvar[0],zvar[-1]])

def init():

    axes[0][0].plot([xvar[0], xvar[-1]], [y0, y0], color=[0.0,0.0,0.0,1.0])
    axes[1][0].plot([xvar[0], xvar[-1]], [z0, z0], color=[0.0,0.0,0.0,1.0])
    axes[0][1].plot([xvar[0], xvar[-1]], [y0, y0], color=[0.0,0.0,0.0,1.0])
    axes[1][1].plot([xvar[0], xvar[-1]], [z0, z0], color=[0.0,0.0,0.0,1.0])

def update(i):
    
    fastForward = 20.0
    t = fastForward*(time.time() - tStart)
    t = t - int(t / (tvar[-1] - tvar[0]))*(tvar[-1] - tvar[0])

    varDisp0.set_data(data0[t,z0,:,:].data)
    varDisp1.set_data(data0[t,:,y0,:].data)
    varDisp2.set_data(data1[t,z0,:,:].data)
    varDisp3.set_data(data1[t,:,y0,:].data)
    # time.sleep(0.1)

anim = animation.FuncAnimation(
    fig,
    update,
    init_func=init,
    frames=atmShape.x*atmShape.y,
    interval = 1)

plt.show(block=False)
