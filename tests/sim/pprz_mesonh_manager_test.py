import sys
sys.path.append('../../')
import os
import threading as th
import numpy as np
import time
import signal

import paparazzi_interface as ppi

def signal_handler(signal, frame):
    print('\nShutting down IVY...')
    try:
        manager.stop()
    except:
        pass
    print("Done.")
    exit()

signal.signal(signal.SIGINT, signal_handler)

print("Starting manager")
manager = ppi.PPRZMesoNHManager()
signal.pause()


