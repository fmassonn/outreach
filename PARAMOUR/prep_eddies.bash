#!/bin/bash

set -o nounset
set -o errexit
set -x

# Years defining the period to build files

yearb=2009
yeare=2011

rootdir=/cofast/phuot/PARAMOUR/EXP/prod_1985_ERA5/outputs/NEMO/

for year in `seq $yearb $yeare`
do
 
  # Oce
  for month in `seq 1 12`
  do
    month=$(printf "%02d" $month)
    file=$rootdir/prod_1985_ERA5_1d_${year}${month}01_${year}${month}??_grid_T.nc
    ls $file
    # Dump variable of interest while sub-selecting the domain
    ncks -F -O -v tos $file tmp_${year}${month}.nc
  done   
done

# Append
ncrcat -F -O tmp_??????.nc tmp.nc
  
# Remap
cdo remapbil,mygrid_0.1x0.1 tmp.nc tmp2.nc

# Crop
ncks -F -O -d lat,100,600 tmp2.nc prod_1985_ERA5_1d_${yearb}0101_${yeare}1231_grid_T_0.1x0.1_cropped.nc
rm -f tmp.nc tmp2.nc tmp_??????.nc



# Ice
for year in `seq $yearb $yeare`
do
  for month in `seq 1 12`
  do
    month=$(printf "%02d" $month)
    file=$rootdir/prod_1985_ERA5_1d_${year}${month}01_${year}${month}??_icemod.nc
    ls $file
    # Dump variable of interest while sub-selecting the domain
    ncks -F -O -v siconc $file tmp_${year}${month}.nc
  done
done

# Append
ncrcat -F -O tmp_??????.nc tmp.nc
# Remap
cdo remapbil,mygrid_0.1x0.1 tmp.nc tmp2.nc

# Crop
ncks -F -O -d lat,100,600 tmp2.nc prod_1985_ERA5_1d_${yearb}0101_${yeare}1231_icemod_0.1x0.1_cropped.nc
rm -f tmp.nc tmp2.nc

# Merge
cp prod_1985_ERA5_1d_${yearb}0101_${yeare}1231_grid_T_0.1x0.1_cropped.nc PARAMOUR.nc
ncks -F -A -v siconc prod_1985_ERA5_1d_${yearb}0101_${yeare}1231_icemod_0.1x0.1_cropped.nc PARAMOUR.nc
