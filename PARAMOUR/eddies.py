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

import matplotlib

# Read data
# Created with prep_eddies.bash
fileIn = "/cofast/fmasson/TMP/TMP2/PARAMOUR.nc"

varList = ["tos", "siconc", "lat", "lon"]

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

for jt in range(time_counter):
    print(str(jt).zfill(3) + "/" + str(time_counter).zfill(3))
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
    levels = np.arange(-2.25, 15.25, step = 1.0)
    #levels = np.array([-2.0 + 0.1 * j for j in range(40)] + [2.0 + 0.5 * j for j in range(20)])
    #cs1 = ax.contourf(lon, lat, data,
    #            transform=ccrs.PlateCarree(),cmap = plt.cm.RdYlBu_r, \
    #                levels = levels, extend = "both")                   
    ax.pcolormesh(lon, lat, data, transform=ccrs.PlateCarree(), cmap = plt.cm.RdYlBu_r, \
                     vmin = levels[0], vmax = levels[-1],)
    #cbar1 = fig.colorbar(cs1)

    # Ice
    data = np.squeeze(siconc[jt, :, :]) 

    # Tweak: the colorbar is linearly going from white to blue but we want
    # it to be non-linear. So we plot the sqrt of siconc instead of siconc
    # itself. Thereby, low values (ex 0.04) are mapped to higher values
    # which are more white.
    data = data ** (1 / 3)
    levels = np.arange(0.0, 1, 0.01)
    ax.pcolormesh(lon, lat, data, transform=ccrs.PlateCarree(), cmap = plt.cm.Greys_r, \
                     vmin = levels[0], vmax = levels[-1],)
    # Add Title
    ax.set_title("1/4° reconstruction of the ocean and sea ice states\nwww.climate.be/paramour")
    plt.savefig("./figs/fig" + str(jt).zfill(5) + ".png")
    
  
    
    plt.close(fig)
    #stop()

