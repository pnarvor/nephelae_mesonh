#! /usr/bin/python3

import os
import sys
sys.path.append("../")
import signal

import ivy_ros_tunnel as irt

tunnel = irt.SimpleIvyRosTunnel()
signal.signal(signal.SIGINT, lambda signal, frame: tunnel.stop())
tunnel.start()

signal.pause()





