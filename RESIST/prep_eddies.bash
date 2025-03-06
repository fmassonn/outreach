#!/bin/bash
#
# Script to pre-process the NEMO output and prepare one file to be read by 
# the python script that makes the plot
# François Massonnet
# 25 April 2024
# Update 10 Dec 2024 for the second eORCA12 run

set -o nounset
set -o errexit
set -x

mymodules_gnu_24_03()
{
         module purge
         module load LUMI/24.03
         module load partition/C
         module load PrgEnv-gnu
         export
MODULEPATH=/project/project_465000898/softs/24.03/modules/all:$MODULEPATH
         module load NCO/5.2.7-cpeGNU-24.03
}

mymodules_elic()
{
    module purge
    #module load ELIC_Python/1-foss-2021b
    module load NCO
    module load CDO
}


if [ $HOSTNAME = "uan01"  ] || [ $HOSTNAME = "uan02" ] || [ $HOSTNAME = "uan04" ]
then
	echo "LOADING NCO"
	mymodules_gnu_24_03
elif [ $HOSTNAME = "aurora" ] || [ $HOSTNAME = "coriolis" ]
then
        mymodules_elic
fi


# Config
machine="lumi"
expname="eorca025_elic_4"
config="${expname}_${machine}"

# Years defining the period to build files

yearb=2024
yeare=2024

if [ $config = "eorca12_elic_2" ]
then
    rootdir=/scratch/project_465001240/barthele/models/nemo/experiments/nemo-4.2.2/eorca12_elic_2/outputs/
    workdir=/scratch/project_465001240/massonne/TMP/
    mkdir -p $workdir
    cd $workdir

    for year in `seq $yearb $yeare`
    do
 
    	for monthStart in 1 4 7 10 #the data is organized in semester
      	do
		monthEnd=$(( $monthStart + 2 ))
 		case $monthEnd in
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
    		monthStart=$(printf "%02d" $monthStart)
    		monthEnd=$(printf "%02d" $monthEnd)
		# Ocean
	 	file=$rootdir/${year}-${monthStart}-01_${year}-${monthEnd}-${endday}/${config}_1d_${year}${monthStart}01_${year}${monthEnd}${endday}_grid_T.nc
		ls $file
		#Dump variable of interest while sub-selecting the domain
		ncks -F -O -v tos $file tmp_${year}_${monthStart}-${monthEnd}.nc

		# Ice
	 	file=$rootdir/${year}-${monthStart}-01_${year}-${monthEnd}-${endday}/${config}_1d_${year}${monthStart}01_${year}${monthEnd}${endday}_icemod.nc
		ncks -F -A -v siconc $file tmp_${year}_${monthStart}-${monthEnd}.nc
	done

	# Append
	ncrcat -F -O tmp_${year}_??-??.nc ${config}_RESIST_${year}.nc
    done

elif [ $config == "eorca1_elic_6_lumi" ] || [ $config == "eorca025_elic_4_lumi" ]
then
    rootdir="/cyfast/brichaud/models/experiments/nemo-4.2.2/${config}/raw/"
    workdir="/cofast/fmasson/TMP/${config}"
    mkdir -p $workdir

    cd $workdir

    for year in `seq $yearb $yeare`
    do
        # Ocean
        file=$rootdir/$year-01-01_$year-12-31/${expname}_1d_${year}0101_${year}1231_grid_T.nc
        ls $file
        #Dump variable of interest while sub-selecting the domain
        ncks -F -O -v tos $file tmp_${year}.nc

        # Ice
        file=$rootdir/$year-01-01_$year-12-31/${expname}_1d_${year}0101_${year}1231_icemod.nc
        ncks -F -A -v siconc $file tmp_${year}.nc

        mv tmp_${year}.nc ${config}_RESIST_${year}.nc
    done
    
fi
