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


    def __init__(self, uavId, t0, mesonhFiles, mesoNHVariables,
                 targetCacheSpan=Fancy()[20, -0.2:0.1, -0.2:0.2, -0.2:0.2],
                 updateThreshold=0.0):

        self.mesonhProbe = MesoNHProbe(MFDataset(mesonhFiles),
                                       mesoNHVariables,
                                       targetCacheSpan,
                                       updateThreshold)
        self.uavId           = uavId
        self.uavPid          = -1
        self.agentName       = None
        self.t0              = t0
        self.currentPosition = []
        self.initialized     = False
        self.stopping        = False
        self.stopped         = False

        IvyInit("MesoNHSensors_" + str(os.getpid()))
        # set log level to hide INFO stdout messages
        logging.getLogger('Ivy').setLevel(logging.WARN) 
        IvyStart("127.255.255.255:2010")
        # try:
        #     print("Bind : ", "'" + '(' + str(self.uavId) + ' GPS .*)' + "'")
        # except Exception as e:
        #     print(e)
        self.gpsBind = IvyBindMsg(lambda agent, msg: self.read_callback_gps(agent, msg),
                                  '(' + str(self.uavId) + ' GPS .*)')
        self.getPidBind = IvyBindMsg(lambda agent, msg: self.get_pid_callback(agent, msg),
                                     '(.* WORLD_ENV_REQ .*)')
        self.reqBind = None
        # self.reqBind = IvyBindMsg(lambda agent, msg: self.read_callback_world(agent, msg),
        #                           '(.* WORLD_ENV_REQ .*)')

    def read_callback_gps(self, ivyAgent, msg):
        
        print("Agent \""+str(ivyAgent)+"\" sent : ", msg)
        # uavId = int(msg.split(' ')[0])
        # if not uavId == self.uavId:
        #     return
        
        
        if self.agentName is None:
            self.agentName = str(ivyAgent)
        
        words = msg.split(' ')
        # self.currentPosition = Fancy()[self.mesonhProbe.t0 + \
        #                                float(words[10]) / 1.0e3 - self.t0,\
        #                                float(words[6])  / 1.0e6,\
        #                                float(words[3])  / 1.0e5,\
        #                                float(words[4])  / 1.0e5]
        t = self.mesonhProbe.t0 + time.time() - self.t0
        self.currentPosition = Fancy()[t,\
                                       float(words[6])  / 1.0e6,\
                                       float(words[3])  / 1.0e5,\
                                       float(words[4])  / 1.0e5]
        if not self.initialized:
            print("Initialization... ", end='')
            self.mesonhProbe.update_cache(self.currentPosition, blocking=True)
            self.initialized = True
            print("Complete !")
            return

    def get_pid_callback(self, ivyAgent, msg):

        if self.agentName is None:
            return
        
        print("Found agent !")
        if str(ivyAgent) == self.agentName and self.uavPid < 0:
            self.uavPid = int(msg.split(' ')[1].split('_')[0])
            print("Bind : ", "'" + '(' + str(self.uavPid) + '_\d+ WORLD_ENV_REQ .*)' + "'")
            self.reqBind = IvyBindMsg(lambda agent, msg: self.read_callback_world(agent, msg),
                                      '(.* ' + str(self.uavPid) + '_\d+ WORLD_ENV_REQ .*)')
            IvyUnBindMsg(self.getPidBind)

    def read_callback_world(self, ivyAgent, msg):
        
        print("Agent \""+str(ivyAgent)+"\" sent : ", msg)
        try:
            words = msg.split(' ')
            uavPid = int(words[1].split("_")[0])
            if not uavPid == self.uavPid:
                return
            # if self.uavId == -1:
            #     self.uavId = int(str(ivyAgent).split(' ')[2].split('@')[0])
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
            for i in range(50):
                if self.stopped:
                    break
                time.sleep(0.1)
        IvyStop()
        self.mesonhProbe.stop()
        print("Complete.")
