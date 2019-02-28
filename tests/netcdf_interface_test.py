#! /usr/bin/python3

import sys
import os
sys.path.append('../')
import numpy as np
import matplotlib.pyplot as plt
import imageio
import matplotlib.cm as cm

from netCDF4 import MFDataset
import netcdf_probe as cdf

"""
Test file for PeriodicContainer and NetCDFInterface types
    - Arguments : MesoNH (netcdf) files to open
"""

mesonhFiles = sys.argv[slice(1,len(sys.argv))]
atm = MFDataset(mesonhFiles)
print('MesoNH opened')

data = cdf.PeriodicContainer(cdf.NetCDFInterface(atm, 'RCT'), [2,3])

# creating a directory for output images
if not os.path.exists("output"):
    os.mkdir("output")
else:
    if not os.path.isdir("output"):
        raise Exception("Cannot use ./output directory. path exist and is not a directory.")

# for t in range(data.shape[0]):
for z in range(data.shape[1]):
    t = z

    image = np.squeeze(data[70,z,0:256,0:256])
    # image = np.squeeze(data[t,50,0:,0:400])

    print("Max RCT value : ", np.amax(image))
    # imageio.imwrite("output/" + str(t).zfill(3) + ".png", cm.viridis(image / np.amax(image))[:,:,0:3])
    imageio.imwrite("output/" + str(t).zfill(3) + ".png", cm.viridis(np.flip(image,0) / 0.0010505)[:,:,0:3])
    print(str(t).zfill(3) + ".png written)")

# Display is crashing when using heavy mesonh files
# plt.imshow(image, cmap='viridis')
# plt.show(block=False)



