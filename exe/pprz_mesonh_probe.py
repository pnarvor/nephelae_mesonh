#! /usr/bin/python3

import sys
import os
sys.path.append('../')
import signal
import argparse

import mesonh_probe as cdf

parser = argparse.ArgumentParser()
parser.add_argument("uav_id", type=int,
                    help="Paparazzi sim UAV id to get GPS message from")
parser.add_argument("t0_sim", type=float,
                    help="Time of beginning of paparazzi simulation for "
                         "synchronization with the MesoNH time")
parser.add_argument("-m", "--mesonh-variables", nargs='+',
                    help="String id of variable to read in the mesonh files")
parser.add_argument("-f", "--mesonh-files", nargs='+',
                    help="MesoNH files to fly the simulated UAV into")
args = parser.parse_args()
print("UAV id           : ", args.uav_id)
print("T0 simulation    : ", args.t0_sim)
print("MesoNH variables : ", args.mesonh_variables)
print("MesoNH files     : ", args.mesonh_files)

if args.mesonh_variables is None:
    raise Exception("Argument error : Mush give at leat one mesonh variable. "
                     "See \"--help\" for details.")
if args.mesonh_files is None:
    raise Exception("Argument error : Mush give at leat one mesonh file. "
                     "See \"--help\" for details.")


probe = cdf.PPRZMesoNHInterface(args.uav_id, args.t0_sim,
                                args.mesonh_files, args.mesonh_variables)


def signal_handler(signal, frame):
    probe.stop()
    exit()
signal.signal(signal.SIGINT, signal_handler)

signal.pause()
