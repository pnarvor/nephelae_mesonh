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

for t in range(data.shape[0]):
    image = np.squeeze(data[t,80,0:800,0:800])
    imageio.imwrite("output/" + str(t).zfill(3) + ".png", cm.viridis(image / np.amax(image))[:,:,0:3])
    print(str(t).zfill(3) + ".png written)")

# Display is crashing when using heavy mesonh files
# plt.imshow(image, cmap='viridis')
# plt.show(block=False)



