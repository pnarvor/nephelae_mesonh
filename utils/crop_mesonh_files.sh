#! /bin/bash

set -e

input_prefix=/net/skyscanner/volume1/data/Nephelae/MesoNH-2019-10/L12zo.1.BOMEX.OUT.
output_prefix=/media/M3-data2/Nephelae/MesoNH02/L12zo.1.BOMEX.OUT.

for i in $(seq 1 360)
do
    j=$((i-1))
    echo "Processing \"$input_prefix$(seq -f "%03g" $i $i).nc\""
    ncks -d ni,0,512 -d nj,0,512 -d ni_u,0,512 -d nj_u,0,512 -d ni_v,0,512 -d nj_v,0,512 $input_prefix$(seq -f "%03g" $i $i).nc $output_prefix$(seq -f "%03g" $j $j).nc
    echo "Created    \"$output_prefix$(seq -f "%03g" $j $j).nc\""
done
