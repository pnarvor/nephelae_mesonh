#! /usr/bin/python3

import os
import sys
sys.path.append("../")
import signal

import ivy_ros_tunnel as irt

finder = irt.IvyAgentFinder()
signal.signal(signal.SIGINT, lambda signal, frame: finder.stop())
finder.start()

signal.pause()





