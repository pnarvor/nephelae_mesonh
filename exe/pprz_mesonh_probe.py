#! /usr/bin/python3

import sys
import os
sys.path.append('../')
import numpy as np
import time
import signal
import argparse

from netCDF4 import MFDataset
sys.path.append('../../netcdf-probe/')
import netcdf_probe as cdf

def signal_handler(signal, frame):
    print('\nShutting down IVY...')
    ivy.shutdown()
    print("Done.")
    exit()

global mesonhProbe # probe read of mesonh with cache
global uavID       # id of UAV messages
global uavT0       # First time of UAV (find a better way)
global initialized # true if cache has beean loaded once
initialized = False

def mesonh_read_callback(ivyComponentId, msg):

    global mesonhProbe
    global uavID
    global uavT0
    global initialized
    
    if not ivyComponentId == uavID:
        return

    if not initialized:
        print("Initializing... ")
        uavT0 = float(msg._fieldvalues[8]) / 1000.0
        position = cdf.Fancy()[mesonhProbe.t0, \
                               float(msg._fieldvalues[4]) / 1.0e6, \
                               float(msg._fieldvalues[1]) / 1.0e5, \
                               float(msg._fieldvalues[2]) / 1.0e5]
        mesonhProbe.update_cache(position, blocking=True)
        initialized = True
        print("Done !")
        return
    position = cdf.Fancy()[mesonhProbe.t0 + float(msg._fieldvalues[8])/1000.0 - uavT0, \
                           float(msg._fieldvalues[4]) / 1.0e6, \
                           float(msg._fieldvalues[1]) / 1.0e5, \
                           float(msg._fieldvalues[2]) / 1.0e5]

    # print(" ------- Position : ", position)
    try:
        print("Read : ", position, ", ", mesonhProbe[position])
    except Exception as e:
        print("Could not read : ", e)
    
    # print(msg._name)
    # print("Got new message:\n",
    #       " - ac_id        : ", ivyComponentId, "\n",
    #       " - name         : ", msg._name, "\n",
    #       " - component id : ", msg._component_id, "\n",
    #       " - field names  :\n", msg._fieldnames, "\n"
    #       " - field coefs  :\n", msg._fieldcoefs, "\n"
    #       " - field types  :\n", msg._fieldtypes, "\n"
    #       " - field values :\n", msg._fieldvalues, "\n")

# initializating paparazzi interface
PPRZ_HOME = os.getenv("PAPARAZZI_HOME")
sys.path.append(PPRZ_HOME + "/var/lib/python")
from pprzlink.ivy import IvyMessagesInterface
from pprzlink.message import PprzMessage
signal.signal(signal.SIGINT, signal_handler)

mesonhfiles = sys.argv[slice(1,len(sys.argv))]
atm = MFDataset(mesonhfiles)
print("MesoNH loaded !")
mesonhProbe = cdf.MesoNHProbe(atm, ['RCT','WT','UT','VT'])
mesonhProbe._MesoNHProbe__targetCacheSpan = cdf.Fancy()[20, -0.2:0.1, -0.2:0.2, -0.2:0.2]
mesonhProbe._MesoNHProbe__updateThreshold = 0.0

# hard value for tests
uavID = 100
ivy = IvyMessagesInterface("MesoNHSensors_" + str(uavID))
ivy.subscribe(mesonh_read_callback,'(.* GPS .*)')

signal.pause()
