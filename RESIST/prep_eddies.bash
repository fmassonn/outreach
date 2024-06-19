#!/bin/bash
#
# Script to pre-process the NEMO output and prepare one file to be read by 
# the python script that makes the plot
# François Massonnet
# 25 April 2024

set -o nounset
set -o errexit
set -x

if [ $HOST = "uan01"  ] || [ $HOST = "uan02" ]
then
	echo "LOADING NCO"
	loadNCO
fi

# Years defining the period to build files

yearb=1961
yeare=1961

rootdir=/scratch/project_465000898/barthele/models/nemo/experiments/nemo-4.2.2/eorca12_elic/outputs/
workdir=/scratch/project_465000898/massonne/TMP/

cd $workdir

for year in `seq $yearb $yeare`
do
 
	for month in `seq 1 9`
  	do
 		case $month in
			1 | 3 | 5 | 7 | 8 | 10 | 12)
      				endday=31
	      			;;
			4 | 6 | 9 | 11)
				endday=30
				;;
			*)
				date -d $year-02-29 &>/dev/null && endday=29 || endday=28
				;;
		esac
    		month=$(printf "%02d" $month)

		# Ocean
	 	file=$rootdir/${year}-${month}-01_${year}-${month}-${endday}/eorca12_elic_1d_${year}${month}01_${year}${month}${endday}_grid_T.nc
		ls $file
		#Dump variable of interest while sub-selecting the domain
		ncks -F -O -v tos $file tmp_${year}${month}.nc

		# Ice
	 	file=$rootdir/${year}-${month}-01_${year}-${month}-${endday}/eorca12_elic_1d_${year}${month}01_${year}${month}${endday}_icemod.nc
		ncks -F -A -v siconc $file tmp_${year}${month}.nc
	done

	# Append
	ncrcat -F -O tmp_${year}??.nc RESIST_${year}.nc
done
