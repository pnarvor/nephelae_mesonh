import os
import sys
import numpy as np
from netCDF4 import MFDataset

from .MesoNHProbe import MesoNHProbe
from .Fancy       import Fancy

PPRZ_HOME = os.getenv("PAPARAZZI_HOME")
sys.path.append(PPRZ_HOME + "/var/lib/python")
from pprzlink.ivy import IvyMessagesInterface
from pprzlink.message import PprzMessage

class PPRZMesoNHInterface(MesoNHProbe):


    def __init__(self, uavID, t0, mesonhFiles, mesoNHVariables,
                 targetCacheSpan=Fancy()[20, -0.2:0.1, -0.2:0.2, -0.2:0.2],
                 updateThreshold=0.0):
        self.mesonhProbe = MesoNHProbe(MFDataset(mesonhFiles),
                                       mesoNHVariables,
                                       targetCacheSpan,
                                       updateThreshold)
        self.uavID = uavID
        self.t0 = t0
        self.initialized = False
        self.ivy = IvyMessagesInterface("MesoNHSensors_" + str(self.uavID))
        self.ivy.subscribe(self.read_callback,'(.* GPS .*)')

    def read_callback(self, ivyAgent, msg):
        
        if not ivyAgent == self.uavID:
            return

        if not self.initialized:
            print("Initializing... ")
            position = Fancy()[self.mesonhProbe.t0, \
                               float(msg._fieldvalues[4]) / 1.0e6, \
                               float(msg._fieldvalues[1]) / 1.0e5, \
                               float(msg._fieldvalues[2]) / 1.0e5]
            self.mesonhProbe.update_cache(position, blocking=True)
            self.initialized = True
            print("Done !")
            return

        position = Fancy()[self.mesonhProbe.t0
                           + float(msg._fieldvalues[8])/1000.0 - self.t0, \
                           float(msg._fieldvalues[4]) / 1.0e6, \
                           float(msg._fieldvalues[1]) / 1.0e5, \
                           float(msg._fieldvalues[2]) / 1.0e5]
        # print(" ------- Position : ", position)
        try:
            print("Read : ", position, ", ", self.mesonhProbe[position])
        except Exception as e:
            print("Could not read : ", e)

    def stop(self):
        print("\nShutting down...")
        self.ivy.shutdown()
        self.mesonhProbe.stop()
        print("Done !")
