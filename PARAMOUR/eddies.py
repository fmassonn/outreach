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
fileIn = "/Users/massonnetf/prod_1985_ERA5_1d_20091201_20091231_icemod_0.25x0.25.nc"

varList = ["siconc", "lat", "lon"]

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
    print(jt)
    fig, _ = plt.subplots(figsize=(6, 6), dpi=300)
    plt.axis('off')
    
    myProj =  ccrs.NearsidePerspective(central_longitude= 0.0 - jt, \
                                      central_latitude=-73.0, \
                                      satellite_height=3000000, \
                                      false_easting=0, false_northing=0)
        
    #myProj = ccrs.Orthographic(central_latitude=-90.0)
    #myProj  = ccrs.SouthPolarStereo()
    ax = plt.axes(projection = myProj)
    
    
    #xlims = [-180,180]
    #ylims = [-90,-73]
    #ax.set_extent(xlims+ylims, crs=ccrs.PlateCarree())
    #ax.set_boundary(circle, transform=ax.transAxes)
    ax.stock_img()
    # Plot Data
    
    tos[tos == 0.0] = np.nan
    siconc[siconc < 0.05] = np.nan
    
    data = np.squeeze(tos[jt,:,:])
    
    
    #ax.stock_img()
    #ax.coastlines("110m", linewidth=0.5, color="black")
    
    #ax.pcolormesh(nav_lon, nav_lat, data,  transform=ccrs.PlateCarree(),  \
    #                   vmin = -2, vmax = 4)
    
    ax.pcolormesh(lon, lat, data,  transform=ccrs.PlateCarree(),  \
                      vmin = -2.0, vmax = 10.0, cmap = plt.cm.RdYlBu_r )
                   
    data = np.squeeze(siconc[jt, :, :])
    ax.pcolormesh(lon, lat, data, \
                   transform=ccrs.PlateCarree(), cmap = plt.cm.Blues_r,
                   vmin = 0.2, vmax = 1.0
                   )
   
    # Add Title
    
    plt.savefig("./figs/fig" + str(jt).zfill(5) + ".png")
    

    plt.close(fig)

