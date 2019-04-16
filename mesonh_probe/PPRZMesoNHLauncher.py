import os
import sys
import sh
import numpy as np
import signal

from .Fancy       import Fancy

PPRZ_HOME = os.getenv("PAPARAZZI_HOME")
sys.path.append(PPRZ_HOME + "/var/lib/python")
from pprzlink.ivy import IvyMessagesInterface
from pprzlink.message import PprzMessage

class PPRZMesoNHLauncher:

    def __init__(self, mesonhFiles, mesonhVariables):

        self.mesonhFiles     = mesonhFiles
        self.mesonhVariables = mesonhVariables
        self.probeExePath = (os.path.dirname(os.path.realpath(__file__))
                             + "/../exe/pprz_mesonh_probe.py")
        self.probes = []
        self.uavT0 = -1.0
        self.uavIDs = []

        self.ivy = IvyMessagesInterface("MesoNHSensors_" + str(os.getpid()))
        self.ivy.subscribe(self.find_uavs_callback,'(.* GPS .*)')

    def stop(self):
        print("\nShutting down...")
        self.ivy.shutdown()
        for p in self.probes:
            p.signal(signal.SIGINT)
        print("Done !")

    def find_uavs_callback(self, ivyAgent, msg):

        if self.uavT0 < 0.0:
            if not float(msg._fieldvalues[8])/1000.0 > 5.0:
                return
            self.uavT0 = float(msg._fieldvalues[8])/1000.0
            print("Setting t0 : ", self.uavT0)
        
        if not ivyAgent in self.uavIDs:
            print("Found UAV : ", ivyAgent)
            self.uavIDs.append(ivyAgent)
            self.launch_probe(ivyAgent)

    def launch_probe(self, uavID):
        command = sh.Command(self.probeExePath)
        command = command.bake(_bg=True, _bg_exc=False,
                               _out="stdout_" + str(uavID) + ".txt",
                               _err="stdout_" + str(uavID) + ".txt")
        # command = command.bake(_bg=True, _bg_exc=False)
        self.probes.append(command(str(uavID),
                                   "-t", str(self.uavT0),
                                   "-m",self.mesonhVariables,
                                   "-f", self.mesonhFiles))
        print("Probe launch successfull")
