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
from matplotlib.collections import LineCollection
from copy import copy



# Import Cartopy
import cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from   cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from cartopy.mpl.patch import geos_to_path

from cartopy.util import add_cyclic_point
import itertools

g = 9.81

# Read data
fileIn = "./Z500.nc"

varList = ["z", "latitude", "longitude", "time"]

f = Dataset(fileIn, mode = "r")

# Read variables
for var in f.variables:
  if var in varList:
    exec(f"{var} = f.variables[var][:].data")

f.close()

z = z /  g  / 10 # to dam
longitude,latitude = np.meshgrid(longitude, latitude)           


# Load coastlines
# https://stackoverflow.com/questions/23785408/3d-cartopy-similar-to-matplotlib-basemap
feature = cartopy.feature.NaturalEarthFeature('physical', 'coastline', '110m')
geoms = feature.geometries()
target_projection = ccrs.PlateCarree()
geoms = [target_projection.project_geometry(geom, feature.crs)
         for geom in geoms]
paths = list(itertools.chain.from_iterable(geos_to_path(geom) for geom in geoms))
segments = []
for path in paths:
    vertices = [vertex for vertex, _ in path.iter_segments()]
    vertices = np.asarray(vertices)
    segments.append(vertices)
lc = LineCollection(segments, color='black')



for jt in range(len(time)):
    print(str(jt) + "/" + str(len(time)))
    fig = plt.subplots( dpi = 300, figsize = (6, 6),)
    ax  = plt.axes(projection = '3d')
    ax.view_init(20, -60)
    myProj =  ccrs.NearsidePerspective(central_longitude= 0.0, \
                                          central_latitude=43.0, \
                                          satellite_height=3000000, \
                                          false_easting=0, false_northing=0)
            
    #ax = plt.axes(projection = myProj)
        
        
    # Continents etc.
    #ax.stock_img()
    
    data = np.squeeze(z[jt,:,:])
    levels = [560, 580]
    #ax.pcolormesh(longitude, latitude, data, transform=ccrs.PlateCarree(), \
    #              cmap = plt.cm.RdYlBu_r, \
    #                     vmin = levels[0], vmax = levels[-1],alpha = 0.5)    
    ax.plot_surface(longitude, latitude, data, cmap=plt.cm.coolwarm,
                           linewidth=0, antialiased=False, alpha = 0.8)
    newLc = copy(lc)
    ax.add_collection3d(newLc)

    ax.set_xlim(np.min(longitude), np.max(longitude))
    ax.set_ylim(np.min(latitude), np.max(latitude))
    ax.set_zlim(0, 1200)
    plt.savefig("./figs/fig" + str(jt).zfill(3) + ".png")
        
      
    stop()
        
    #plt.close(fig)

