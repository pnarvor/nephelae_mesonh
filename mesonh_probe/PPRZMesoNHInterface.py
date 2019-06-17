import os
import sys
import numpy as np
from netCDF4 import MFDataset
import utm

from .MesoNHProbe import MesoNHProbe
from .Fancy       import Fancy

# PPRZ_HOME = os.getenv("PAPARAZZI_HOME")
# sys.path.append(PPRZ_HOME + "/var/lib/python")
# from pprzlink.ivy import IvyMessagesInterface
# from pprzlink.message import PprzMessage

from ivy.std_api import *
import logging

class PPRZMesoNHInterface(MesoNHProbe):


    def __init__(self, simPid, t0, mesonhFiles, mesoNHVariables,
                 targetCacheSpan=Fancy()[20, -0.2:0.1, -0.2:0.2, -0.2:0.2],
                 updateThreshold=0.0):

        self.mesonhProbe = MesoNHProbe(MFDataset(mesonhFiles),
                                       mesoNHVariables,
                                       targetCacheSpan,
                                       updateThreshold)
        self.simPid = simPid
        self.uavID  = -1
        self.t0 = t0
        self.currentPosition = []
        self.initialized = False

        IvyInit("MesoNHSensors_" + str(os.getpid()))
        # set log level to hide INFO stdout messages
        logging.getLogger('Ivy').setLevel(logging.WARN) 
        IvyStart("127.255.255.255:2010")
        IvyBindMsg(lambda agent, msg: self.read_callback_gps(agent, msg),
                   '(.* GPS .*)')
        IvyBindMsg(lambda agent, msg: self.read_callback_world(agent, msg),
                   '(.* WORLD_ENV_REQ .*)')

    def read_callback_gps(self, ivyAgent, msg):
        
        # print("Agent \""+str(ivyAgent)+"\" sent : ", msg)
        uavId = int(msg.split(' ')[0])
        if not uavId == self.uavID:
            return

        words = msg.split(' ')
        self.currentPosition = Fancy()[self.mesonhProbe.t0 + \
                                       float(words[10]) / 1.0e3 - self.t0,\
                                       float(words[6])  / 1.0e6,\
                                       float(words[3])  / 1.0e5,\
                                       float(words[4])  / 1.0e5]
        if not self.initialized:
            print("Initialization... ", end='')
            self.mesonhProbe.update_cache(self.currentPosition, blocking=True)
            self.initialized = True
            print("Complete !")
            return

    def read_callback_world(self, ivyAgent, msg):
        
        # print("Agent \""+str(ivyAgent)+"\" sent : ", msg)
        words = msg.split(' ')
        simPid = int(words[1].split("_")[0])
        if not simPid == self.simPid:
            return
        if self.uavID == -1:
            self.uavID = int(str(ivyAgent).split(' ')[2].split('@')[0])
        if not self.initialized:
            return

        values = []
        try:
            values = self.mesonhProbe[self.currentPosition]
        except Exception as e:
            print("Could not read : ", e)
            print("Position : ", self.currentPosition)
            return

        # print("Read : ", self.currentPosition, ", ", values)
        
        response = (words[1] + " " + words[0] + " WORLD_ENV "
                    + str(values[2]) + " " + str(values[3]) + " " + str(values[1]) + " 266.0 1.0 1")
        # response = (words[1] + " " + words[0] + " WORLD_ENV "
        #             + str(0.0) + " " + str(0.0) + " " + str(0.0) + " 266.0 1.0 1")
        print("Response : ", response)
        IvySendMsg(response)

    def stop(self):
        print("\nShutting down... ", end="")
        IvyStop()
        self.mesonhProbe.stop()
        print("Complete.")
