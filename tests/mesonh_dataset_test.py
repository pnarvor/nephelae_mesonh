#! /usr/bin/python3

import sys
sys.path.append('../')

from nephelae_mesonh import MesonhDataset

import numpy as np

# mesonhFiles = '/home/pnarvor/work/nephelae/data/MesoNH-2019-02/REFHR.1.ARMCu.4D.nc'
mesonhFiles = '/home/pnarvor/work/nephelae/data/nephelae-remote/MesoNH02/bomex_hf.nc'

dataset = MesonhDataset(mesonhFiles)




