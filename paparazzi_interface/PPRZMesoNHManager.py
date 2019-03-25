import sys
sys.path.append('../')
import os
import threading as th
import numpy as np
import time
import signal

# initializating paparazzi interface
PPRZ_HOME = os.getenv("PAPARAZZI_HOME")
sys.path.append(PPRZ_HOME + "/var/lib/python")
from pprzlink.ivy import IvyMessagesInterface
from pprzlink.message import PprzMessage

def callback_test(ivyComponentId, msg):

    aircrafts = []
    for id in msg._fieldvalues[0]:
        aircrafts.append(int(id))

    print("Got aircrafts : ", aircrafts)

    # print(msg._name)
    # print("Got new message from ", str(ivyComponentId), " :\n",
    #       " - ac_id        : ", ivyComponentId, "\n",
    #       " - name         : ", msg._name, "\n",
    #       " - component id : ", msg._component_id, "\n",
    #       " - field names  :\n", msg._fieldnames, "\n"
    #       " - field coefs  :\n", msg._fieldcoefs, "\n"
    #       " - field types  :\n", msg._fieldtypes, "\n"
    #       " - field values :\n", msg._fieldvalues, "\n")

class PPRZMesoNHManager(th.Thread):

    """
    Class to query current pprz uavs on ivy bus and launch an associated
    (eventually remote) MesoNHProbe
    """


    def __init__(self):
        super(PPRZMesoNHManager, self).__init__(name="PPRZMesoNHManager-{}".format(id(self)))

        self.__running = False
        self.__requestCount = 0

        self.ivy = IvyMessagesInterface("MesoNHProbeManager_" + str(os.getpid()),
                                        ivy_bus="127.255.255.255:2010")
        # self.ivy.subscribe(callback_test,'(.* GPS .*)')
        # self.ivy.subscribe(callback_test,'(.* AIRCRAFTS_REQ .*)')
        # self.ivy.subscribe(callback_test,'(.*)')
        self.ivy.subscribe(callback_test,'(.* AIRCRAFTS .*)')

        self.start()

    def stop(self):
        self.ivy.shutdown()
        self.__running = False
        self.join()
    
    def run(self):
        print("Manager started !")

        self.__running = True
        while self.__running:
            # msg = PprzMessage("ground", "AIRCRAFTS_REQ", os.getpid())
            msg = ("MesoNHProbeManager " + str(os.getpid()) + "_"
                   + str(self.__requestCount) + " AIRCRAFTS_REQ")
            self.ivy.send(msg)
            self.__requestCount = self.__requestCount + 1
            time.sleep(1.0)
        print("Manager stopped !")

        
