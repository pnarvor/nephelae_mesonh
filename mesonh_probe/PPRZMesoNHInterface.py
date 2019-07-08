import os
import sys
import numpy as np
from netCDF4 import MFDataset
import utm
import time

from nephelae_simulation.mesonh_interface import MesoNHVariable
from nephelae_paparazzi.pprzinterface.messages import Message
from nephelae_paparazzi.pprzinterface.messages import WorldEnvReq
from nephelae_paparazzi.pprzinterface.messages import WorldEnv
from .MesoNHCachedProbe import MesoNHCachedProbe
from .Fancy             import Fancy

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

        self.reqBind = WorldEnvReq.bind(self.read_callback_world, self.uavPid)


    def read_callback_world(self, msg):
        
        print(msg)
        t = msg.stamp - self.t0

        position = Fancy()[t,msg.alt, msg.utm_north, msg.utm_east]
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

        print("Read : ", position, ", ", values, end="\n\n")
        
        if not self.stopping:
            response = WorldEnv.build(msg, values[0], values[1], values[2])
        else:
            # sending 0s for stopping wind
            if self.reqBind is not None:
                Message.unbind(self.reqBind)
                self.reqBind = None
            response = WorldEnv.build(msg, 0.0, 0.0, 0.0)
            self.stopped = True
        print("Response : ", response)
        response.send() 

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
        for probe in self.probes:
            probe.stop()
        print("Complete.")
