#! /usr/bin/python3

import os
import sys
import signal

def signal_handler(signal, frame):
    print("\nShutdown... ", end='')
    IvyStop()
    print("Complete.")
    exit()
signal.signal(signal.SIGINT, signal_handler)




# IvyBus related code starts here ################################

from ivy.std_api import *
import logging

IvyInit("Ivy_sniffer_" + str(os.getpid()))      # Ivy Agent initialization
logging.getLogger('Ivy').setLevel(logging.WARN) # set log level to hide INFO stdout messages
IvyStart("127.255.255.255:2010")                # IvyBus on localhost

def callback_01(agent, msg):
    print("Agent \"" + str(agent) + "\" sent : \"" + str(msg) + "\"")
# IvyBindMsg(callback_01, '(.*)')
# IvyBindMsg(callback_01, '(.* GPS .*)') # Binding a callback to a regex (regular expression) filter
# IvyBindMsg(callback_01, '(.*PAYLOAD_FLOAT_PPRZ.*)') # Binding a callback to a regex (regular expression) filter
# IvyBindMsg(callback_01, '(.*PAYLOAD_FLOAT_MBED.*)') # Binding a callback to a regex (regular expression) filter
# IvyBindMsg(callback_01, '(.*test.*)')

IvyBindMsg(callback_01, '(.* WORLD_ENV.*)') # Binding a callback to a regex (regular expression) filter


# IvyBus related code stops here #################################




signal.pause()










