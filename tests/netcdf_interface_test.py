#! /usr/bin/python3

import sys
sys.path.append('../')
import numpy as np
import matplotlib.pyplot as plt

from netCDF4 import MFDataset
import netcdf_probe as cdf

mesonhFiles = sys.argv[slice(1,len(sys.argv))]
atm = MFDataset(mesonhFiles)

data = cdf.PeriodicContainer(cdf.NetCDFInterface(atm, 'RCT'), [2,3])
image = np.squeeze(data[0,80,0:400,0:400])

implot = plt.imshow(image, cmap='viridis')

plt.show(block=False)



