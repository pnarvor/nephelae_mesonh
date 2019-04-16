#! /bin/bash

/home/pnarvor/work/nephelae/soft/paparazzi/sw/simulator/pprzsim-launch -b 127.255.255.255 -a Microjet_neph_0 -t sim --boot --norc &
/home/pnarvor/work/nephelae/soft/paparazzi/sw/simulator/pprzsim-launch -b 127.255.255.255 -a Microjet_neph_1 -t sim --boot --norc &
/home/pnarvor/work/nephelae/soft/paparazzi/sw/ground_segment/cockpit/gcs -layout large_left_col.xml &
/home/pnarvor/work/nephelae/soft/paparazzi/sw/ground_segment/tmtc/server -n


