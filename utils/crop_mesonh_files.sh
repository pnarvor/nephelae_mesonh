#! /bin/bash

set -e

start=0
stop=511

input_prefix=/net/skyscanner/volume1/data/Nephelae/MesoNH-2019-10/L12zo.1.BOMEX.OUT.
output_prefix=/media/M3-data2/Nephelae/MesoNH02/L12zo.1.BOMEX.OUT.

for i in $(seq 1 360)
do
    j=$((i-1))
    echo "Processing \"$input_prefix$(seq -f "%03g" $i $i).nc\""
    ncks -d ni,$start,$stop \
         -d nj,$start,$stop \
         -d ni_u,$start,$stop \
         -d nj_u,$start,$stop \
         -d ni_v,$start,$stop \
         -d nj_v,$start,$stop \
         $input_prefix$(seq -f "%03g" $i $i).nc $output_prefix$(seq -f "%03g" $j $j).nc
    echo "Created    \"$output_prefix$(seq -f "%03g" $j $j).nc\""
done
