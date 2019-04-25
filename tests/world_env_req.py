#! /usr/bin/python3

import os
import sys
import signal
import utm

def signal_handler(signal, frame):
    print("Shutdown...")
    IvyStop()
    print("Done.")
    exit()
signal.signal(signal.SIGINT, signal_handler)




# IvyBus related code starts here ################################

from ivy.std_api import *
import logging

UT = 0.0
VT = 0.0
WT = 0.0

IvyInit("Ivy_sniffer_" + str(os.getpid()))      # Ivy Agent initialization
logging.getLogger('Ivy').setLevel(logging.WARN) # set log level to hide INFO stdout messages
IvyStart("127.255.255.255:2010")                # IvyBus on localhost

def callback_01(agent, msg):
    print("Agent \"" + str(agent) + "\" sent : \"" + str(msg) + "\"")
    values = str(msg).split(" ")
    utmPos = utm.from_latlon(float(values[3]), float(values[4]))
    print("UTM : ", utmPos)
    response = (values[1] + " " + values[0] + " WORLD_ENV "
                + str(UT) + " " + str(VT) + " " + str(WT) + " 266.0 1.0 1")
    # print("Response : \"" + response + "\"")
    IvySendMsg(response)

IvyBindMsg(callback_01, '(.* 23244_.* WORLD_ENV_REQ .*)')
# IvyBindMsg(callback_01, '(.* WORLD_ENV_REQ .*)')

# IvyBus related code stops here #################################




# signal.pause()










