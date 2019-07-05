import os
import sys
import numpy as np
from netCDF4 import MFDataset
import utm
import time

from nephelae_simulation.mesonh_interface import MesoNHVariable
from .MesoNHCachedProbe import MesoNHCachedProbe
from .Fancy             import Fancy

from ivy.std_api import *
import logging

class PPRZMesoNHInterface:


    def __init__(self, uavPid, t0, mesonhFiles, mesoNHVariables,
                 targetCacheBounds=[[0,20],[-200,100],[-200,200],[-200,200]],
                 updateThreshold=0.0):

        self.atm    = MFDataset(mesonhFiles)
        self.probes = [MesoNHCachedProbe(
                            MesoNHVariable(self.atm, var, interpolation='linear'),
                            targetCacheBounds, 0.25)
                            for var in mesoNHVariables]

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
        
        # t = self.mesonhProbe.t0 + time.time() - self.t0
        t = time.time() - self.t0
        print("Agent \""+str(ivyAgent)+"\" sent : ", msg)

        try:
            words = msg.split(' ')
            uavPid = int(words[1].split("_")[0])
            if not uavPid == self.uavPid:
                return

            # MesoNH access is [t,z,y,x]
            position = Fancy()[t,float(words[5]),float(words[7]),float(words[6])]
            if not self.initialized:
                print("Initialization... ", end='')
                for probe in self.probes:
                    probe.request_cache_update(position, block=True)
                self.initialized = True
                print("Complete !")
                return

            values = []
            try:
                values = [probe[position] for probe in self.probes]
            except Exception as e:
                # raise e
                print("Could not read : ", e)
                print("Position : ", position)
                return

            print("Read : ", position, ", ", values)
            
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
            raise e
            # print("world exception : ", e)
    

    def start(self):
        for probe in self.probes:
            probe.start()
        

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
        for probe in self.probes:
            probe.stop()
        print("Complete.")
