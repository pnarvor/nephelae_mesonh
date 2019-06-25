import os
import sys
import sh
import numpy as np
import signal
import utm
import time

from .Fancy       import Fancy

from ivy.std_api import *
import logging

class PPRZMesoNHLauncher:

    def __init__(self, mesonhFiles, mesonhVariables):

        self.mesonhFiles     = mesonhFiles
        self.mesonhVariables = ['UT','VT','WT'] + mesonhVariables
        self.probeExePath = (os.path.dirname(os.path.realpath(__file__))
                             + "/../exe/pprz_mesonh_probe.py")
        self.probes = []
        self.uavT0 = -1.0
        self.uavIDs = []

        IvyInit("MesoNHSensors_" + str(os.getpid()))
        # set log level to hide INFO stdout messages
        logging.getLogger('Ivy').setLevel(logging.WARN) 
        IvyStart("127.255.255.255:2010")
        IvyBindMsg(lambda agent, msg: self.find_uavs_callback(agent, msg),
                   '(.* WORLD_ENV_REQ .*)')

    def stop(self):
        print("\nShutting down...", end="")
        for p in self.probes:
            p.signal(signal.SIGINT)
            p.wait()
        self.probes = []
        IvyStop()
        print("Complete.")

    def find_uavs_callback(self, ivyAgent, msg):

        if self.uavT0 < 0.0:
            self.uavT0 = time.time()
            print("t0 : ", self.uavT0)

        # uavId = int(msg.split(' ')[1]) # real uav id
        uavId = int(msg.split(' ')[1].split('_')[0]) # uav sim pid 
        if not uavId in self.uavIDs:
            print("Found UAV : ", uavId)
            self.uavIDs.append(uavId)
            self.launch_probe(uavId)

    def launch_probe(self, uavID):
        command = sh.Command(self.probeExePath)
        command = command.bake(_bg=True, _bg_exc=False,
                               _out="stdout_" + str(uavID) + ".txt",
                               _err="stdout_" + str(uavID) + ".txt")
        self.probes.append(command(str(uavID),
                                   "-t", str(self.uavT0),
                                   "-m", self.mesonhVariables,
                                   "-f", self.mesonhFiles))
        print("Probe launch successfull (pid:"+str(self.probes[-1].pid)+")")



