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

# Plot

#fig, ax = plt.subplots(1, 1, figsize=(6, 6), dpi=150)

# # Define projection
# myProj =ccrs.NearsidePerspective(central_longitude=0.0, \
#                                  central_latitude=0.0,  \
#                                  satellite_height=35785831, \
#                                  false_easting=0, false_northing=0, \
#                                      globe=None)

# ax = plt.axes(projection= myProj)
# xlims = [-180,180]
# ylims = [-90, -60]
# theta = np.linspace(0, 2*np.pi, 100)
# center, radius = [0.5, 0.5], 0.5
# verts = np.vstack([np.sin(theta), np.cos(theta)]).T
# circle = mpath.Path(verts * radius + center)
# ax.set_extent(xlims+ylims, crs=ccrs.Orthographic(-10, 45))
# ax.set_boundary(circle, transform=ax.transAxes)
# ax.stock_img()
# ax.coastlines("110m", linewidth=0.5, color="black")

# #cs = ax.pcolormesh(nav_lon, nav_lat, tos[0, :, :], \
# #                    cmap = plt.cm.Blues_r
# #                   )
# ax.add_feature(cfeature.COASTLINE.with_scale('50m'))

#------------------------------------------------------------
# Compute a circle in axes coordinates, 
# which we can use as a boundary for the map.
# https://scitools.org.uk/cartopy/docs/latest/gallery/lines_and_polygons/always_circular_stereo.html
theta = np.linspace(0, 2*np.pi, 100)
center, radius = [0.5, 0.5], 0.5
verts = np.vstack([np.sin(theta), np.cos(theta)]).T
circle = mpath.Path(verts * radius + center)



for jt in range(time_counter):
    print(jt)
    fig, _ = plt.subplots(figsize=(6, 6), dpi=300)
    plt.axis('off')
    
    myProj =  ccrs.NearsidePerspective(central_longitude= 0.0 + jt, \
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
    
    data = np.squeeze(tos[jt,:,:])
    
    
    #ax.stock_img()
    #ax.coastlines("110m", linewidth=0.5, color="black")
    
    #ax.pcolormesh(nav_lon, nav_lat, data,  transform=ccrs.PlateCarree(),  \
    #                   vmin = -2, vmax = 4)
    
    ax.pcolormesh(lon, lat, data,  transform=ccrs.PlateCarree(),  \
                      vmin = -2.0, vmax = 10.0, cmap = plt.cm.RdYlBu_r )
                       
    
    # Doing the gridlines we want 
    #gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linewidth=0.5, color="grey")
    #gl.xformatter = LONGITUDE_FORMATTER
    #gl.yformatter = LATITUDE_FORMATTER
    #gl.xlocator = mticker.FixedLocator(np.arange(-180,181,18))
    #gl.ylocator = mticker.FixedLocator(np.arange(-90,91,10))
    
    # Add Colorbar
    #cbar = plt.colorbar(cs,orientation="horizontal")
    
    # Add Title
    
    plt.savefig("./figs/fig" + str(jt).zfill(5) + ".png")
    
    plt.close(fig)

