#! /bin/bash

# This script will generate the script to merge files.
# to generate the script : ./stack_mesonh_files > do_merge.sh

# /!\ Hard coded parameters

input_prefix=/media/M3-data2/Nephelae/MesoNH02/L12zo.1.BOMEX.OUT.
output_file=/media/Nephelae-Data/data/Nephelae/MesoNH02/bomex_hf.nc

echo "#! /bin/bash"
echo ""
echo "set -e"
echo ""
echo "cdo mergetime \\"

for i in $(seq -f "%03g" 0 359)
do
    echo "    $input_prefix$i.nc \\"
done
echo "    $output_file"




