# Set of animations and images to show eddies in the 
# 1/4° configuration PARASO from the PARAMOUR
# www.climate.be/paramour
# project.
#
# Author - François Massonnet

from netCDF4 import Dataset
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.ticker as mticker

# Import Cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from   cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from cartopy.util import add_cyclic_point

# Read ocean data
#fileIn = "/cofast/fmasson/TMP/prod_1985_ERA5_1d_20090101_20091231_grid_T_0.25x0.25.nc"
fileIn = "/Users/massonnetf/prod_1985_ERA5_1d_20091201_20091231_grid_T_0.25x0.25.nc"

varList = ["tos", "lat", "lon"]

f = Dataset(fileIn, mode = "r")

# Read dimensions
for dim in f.dimensions:
  #exec("{} = {}".format(dim, range(f.dimensions[dim].size)))
  exec(f"{dim} = f.dimensions[dim].size")
  
# Read variables
for var in f.variables:
  if var in varList:
    exec(f"{var} = f.variables[var][:].data")

f.close()

# Read ice data
#fileIn = "/cofast/fmasson/TMP/prod_1985_ERA5_1d_20090101_20091231_icemod_0.25x0.25.nc"
fileIn = "/Users/massonnetf/prod_1985_ERA5_1d_20091201_20091231_icemod_0.25x0.25.nc"

varList = ["siconc", "lat", "lon"]

f = Dataset(fileIn, mode = "r")

# Read dimensions
for dim in f.dimensions:
  exec(f"{dim} = f.dimensions[dim].size")
  
# Read variables
for var in f.variables:
  if var in varList:
    exec(f"{var} = f.variables[var][:].data")

f.close()


for jt in range(time_counter):
    print(jt)
    fig, _ = plt.subplots(figsize=(6, 6), dpi=300)
    plt.axis('off')
    
    myProj =  ccrs.NearsidePerspective(central_longitude= 0.0 + jt / 10, \
                                      central_latitude=-73.0, \
                                      satellite_height=3000000, \
                                      false_easting=0, false_northing=0)
        
    ax = plt.axes(projection = myProj)
    
    
    # Continents etc.
    ax.stock_img()

    # Plot Data
    
    tos[tos == 0.0] = np.nan
    siconc[siconc < 0.05] = np.nan
    
    data = np.squeeze(tos[jt,:,:])
    
    # SST
    levels = np.arange(-2.0, 10.0, step = 1)
    #levels = np.array([-2.0 + 0.1 * j for j in range(20)] + [2.0 + 1.0 * j for j in range(15)])
    ax.contourf(lon, lat, data,
                transform=ccrs.PlateCarree(),cmap = plt.cm.inferno, \
                    levels = levels, extend = "both")                   


    # Ice
    data = np.squeeze(siconc[jt, :, :]) 

    # Tweak: the colorbar is linearly going from white to blue but we want
    # it to be non-linear. So we plot the sqrt of siconc instead of siconc
    # itself. Thereby, low values (ex 0.04) are mapped to higher values
    # which are more white.
    data = data ** (1 / 3)
    levels = np.arange(0.0, 1, 0.1)
    ax.contourf(lon, lat, data,
                transform=ccrs.PlateCarree(),cmap = plt.cm.Blues_r, \
                    levels = levels, extend = "both")
    # Add Title
    #cs.cmap.set_under(col_under)
    #cs.cmap.set_over(col_over)
    plt.savefig("./figs/fig" + str(jt).zfill(5) + ".png")
    
  
    
    plt.close(fig)
    stop()

