import os
import sys
import numpy as np
from netCDF4 import MFDataset
import utm
import time

from .MesoNHProbe import MesoNHProbe
from .Fancy       import Fancy

# PPRZ_HOME = os.getenv("PAPARAZZI_HOME")
# sys.path.append(PPRZ_HOME + "/var/lib/python")
# from pprzlink.ivy import IvyMessagesInterface
# from pprzlink.message import PprzMessage

from ivy.std_api import *
import logging

class PPRZMesoNHInterface(MesoNHProbe):


    def __init__(self, uavPid, t0, mesonhFiles, mesoNHVariables,
                 targetCacheSpan=Fancy()[20, -0.2:0.1, -0.2:0.2, -0.2:0.2],
                 updateThreshold=0.0):

        self.mesonhProbe = MesoNHProbe(MFDataset(mesonhFiles),
                                       mesoNHVariables,
                                       targetCacheSpan,
                                       updateThreshold)
        self.uavPid          = uavPid
        self.t0              = t0
        self.currentPosition = []
        self.initialized     = False
        self.stopping        = False
        self.stopped         = False

        IvyInit("MesoNHSensors_" + str(os.getpid()))
        # set log level to hide INFO stdout messages
        logging.getLogger('Ivy').setLevel(logging.WARN) 
        IvyStart("127.255.255.255:2010")
        try:
            self.reqBind = IvyBindMsg(lambda agent, msg: self.read_callback_world(agent, msg),
                                      # '(.* ' + str(self.uavPid) + '.*  WORLD_ENV_REQ .*)')
                                      '(.* ' + str(self.uavPid) + '_\d+ WORLD_ENV_REQ .*)')
        except Exception as e:
            print("PPRZMesoNHInterface.__init__ : \"" + str(e) + "\"")

    def read_callback_world(self, ivyAgent, msg):
        
        t = self.mesonhProbe.t0 + time.time() - self.t0
        print("Agent \""+str(ivyAgent)+"\" sent : ", msg)

        try:
            words = msg.split(' ')
            uavPid = int(words[1].split("_")[0])
            if not uavPid == self.uavPid:
                return
            # /!\ Mesonh dimensions are in km ...
            # To be checked for reusability
            position = Fancy()[t,\
                               float(words[6]) / 1.0e3,\
                               float(words[7]) / 1.0e3,\
                               float(words[5]) / 1.0e3]
            if not self.initialized:
                print("Initialization... ", end='')
                self.mesonhProbe.update_cache(position, blocking=True)
                self.initialized = True
                print("Complete !")
                return
            if not self.initialized:
                return

            values = []
            try:
                values = self.mesonhProbe[position]
            except Exception as e:
                print("Could not read : ", e)
                print("Position : ", position)
                return

            # print("Read : ", position, ", ", values)
            
            if not self.stopping:
                response = (words[1] + " " + words[0] + " WORLD_ENV "
                            + str(values[0]) + " "
                            + str(values[1]) + " "
                            + str(values[2]) + " 266.0 1.0 1")
            else:
                # sending 0s for stopping wind
                if self.reqBind is not None:
                    IvyUnBindMsg(self.reqBind)
                    self.reqBind = None
                response = (words[1] + " " + words[0] + " WORLD_ENV "
                            + str(0.0) + " " + str(0.0) + " " + str(0.0)
                            + " 266.0 1.0 1")
                self.stopped = True
            print("Response : ", response)
            IvySendMsg(response)
        except Exception as e:
            print("world exception : ", e)

    def stop(self):
        print("\nShutting down... ", end="")
        if self.reqBind is not None:
            self.stopping = True
            # for i in range(50):
            for i in range(10):
                if self.stopped:
                    break
                time.sleep(0.1)
        IvyStop()
        self.mesonhProbe.stop()
        print("Complete.")
