# Set of animations and images to show eddies in the 
# 1/4° configuration PARASO from the PARAMOUR
# www.climate.be/paramour
# project.
#
# Author - François Massonnet

from netCDF4 import Dataset
import numpy as np

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.ticker as mticker

# Import Cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from   cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from cartopy.util import add_cyclic_point
import xarray as xr
import matplotlib

from   matplotlib.colors import LinearSegmentedColormap



# Read data
# Created with prep_eddies.bash

expname = "eorca025_elic_4"
machine = "lumi"
config  = expname + "_" + machine
if expname == "eorca1_elic_6":
   strReso = "1°"
elif expname == "eorca025_elic_4":
   strReso = "1/4°"
elif expname == "eorca12_elic":
   strReso = "1/12°"

rotatingEarth= True

yearb, yeare = 2015, 2024

for year in range(yearb, yeare + 1): # 1997--2004 works
    
    fileIn = "/scratch/project_465001240/massonne/TMP/RESIST_" + str(year) + ".nc"
    fileIn = "/cofast/fmasson/TMP/" + config + "/" + config + "_RESIST_" + str(year) + ".nc"
    dimTime = "time_counter"
    
    varConcStr = "siconc"
    varTosStr  = "tos"
    
    ds = xr.open_dataset(fileIn)
    nt = ds.dims[dimTime]
    
    # Get the time-invariant lat/lon fields
    
    lon = ds.variables["nav_lon"].values
    lat = ds.variables["nav_lat"].values
    
    for jt in range(nt):
        for region in ["Arctic", "Antarctic"]:
            print(str(jt).zfill(3) + "/" + str(nt).zfill(3))
            t=ds.variables["time_counter"][jt].values
            stringTime = np.datetime_as_string(t, unit='D')
        
            concShow = ds.isel(time_counter = jt).variables[varConcStr].values
            tosShow = ds.isel(time_counter = jt).variables[varTosStr].values
        
            fig, _ = plt.subplots(figsize=(6, 6), dpi=300)
            plt.axis('off')
            
            offsetMap = (t - np.datetime64("1960-01-01T12:00:00.000000000")).item() / 86400000000000

            if not rotatingEarth:
                offsetMap = 0 * offsetMap 
 
            if region == "Arctic":
                central_latitude = +73.0
            elif region == "Antarctic":
                central_latitude = - 73.0

            myProj =  ccrs.NearsidePerspective(central_longitude= 0.0 + offsetMap / 10, \
                                              central_latitude=central_latitude, \
                                              satellite_height=3000000, \
                                              false_easting=0, false_northing=0)
                
            ax = plt.axes(projection = myProj)
            
            
            # Continents etc.
            ax.stock_img()
        
            # Plot Data
            
            tosShow[tosShow == 0.0] = np.nan
            concShow[concShow < 0.05] = np.nan
                
            # SST
            levels = np.arange(-2.25, 15.25, step = 1.0)
            #levels = np.array([-2.0 + 0.1 * j for j in range(40)] + [2.0 + 0.5 * j for j in range(20)])
            #cs1 = ax.contourf(lon, lat, data,
            #            transform=ccrs.PlateCarree(),cmap = plt.cm.RdYlBu_r, \
            #                levels = levels, extend = "both")                   
            ax.pcolormesh(lon, lat, tosShow, transform=ccrs.PlateCarree(), cmap = plt.cm.RdYlBu_r, \
                             vmin = levels[0], vmax = levels[-1],)
            #cbar1 = fig.colorbar(cs1)
        
            # Ice
        
        
            # Tweak: the colorbar is linearly going from white to blue but we want
            # it to be non-linear. So we plot the sqrt of siconc instead of siconc
            # itself. Thereby, low values (ex 0.04) are mapped to higher values
            # which are more white.
            #data = data ** (1 / 3)
            sourceColors = [ [0.0, 0.0, 0.2], [0.95, 0.95, 0.95]]
            myCM = LinearSegmentedColormap.from_list('myCM', sourceColors, N = 100)
        
            #levels = np.arange(0.0, 1, 0.01)
            levels = np.arange(0.0, 1.05, 0.05)
        
            ax.pcolormesh(lon, lat, concShow, transform=ccrs.PlateCarree(), cmap = myCM, \
                             vmin = levels[0], vmax = levels[-1],)
            # Add Title
            ax.set_title(strReso + " reconstruction of the ocean and sea ice states\nwww.resist-project.github.io\n" + stringTime)

            if rotatingEarth:
                folder = "./figs/" + config + "/" + region + "/rotating/" 
            else:
                folder = "./figs/" + config + "/" + region + "/fixed/" 

            Path(folder).mkdir(parents=True, exist_ok=True)

            print("Saving " + folder + "/" + stringTime + ".png")
            plt.savefig(folder + "/" + stringTime + ".png")
            
          
            
            plt.close(fig)
            #stop()
        
