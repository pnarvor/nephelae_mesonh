#! /usr/bin/python3

import sys
sys.path.append('../')
import numpy as np

from mesonh_interface import DimensionHelper
from mesonh_probe     import Fancy

dim0 = np.linspace(0.0,4.0,5)
dim1 = dim0**2


dims = DimensionHelper()
# dims.add_dimension(dim0, 'affine')
dims.add_dimension(dim0, 'LUT')



