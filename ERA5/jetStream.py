import matplotlib.pyplot as plt
import numpy as np

import cartopy.crs as ccrs
import cartopy.feature as cfeature

from netCDF4 import Dataset
import datetime
from datetime import timedelta

refDateNetcdf = datetime.datetime(1900, 1, 1)


f = Dataset("download_UVP.nc", mode = "r")
s = f.variables["s"][:]
lon=f.variables["longitude"][:]
lat=f.variables["latitude"][:]
t  =f.variables["time"][:]
f.close()


for jt in range(len(t)):
    thisDate = refDateNetcdf + timedelta(days = t[jt] / 24)
    print(thisDate)
    print(jt)
    fig, _ = plt.subplots(figsize=(6, 6), dpi=300)
    plt.axis('off')

    myProj =  ccrs.NearsidePerspective(central_longitude= 4.0 + 0 * jt / 10, \
                                      central_latitude=51.0, \
                                      satellite_height=3000000, \
                                      false_easting=0, false_northing=0)

    ax = plt.axes(projection = myProj)


    # Continents etc.
    ax.stock_img()

    # Plot Data

    data = np.squeeze(s[jt,:,:])
    
    # SST
    levels = np.arange(20, 60, step = 1.0)
    #levels = np.array([-2.0 + 0.1 * j for j in range(40)] + [2.0 + 0.5 * j for j in range(20)])
    #cs1 = ax.contourf(lon, lat, data,
    #            transform=ccrs.PlateCarree(),cmap = plt.cm.RdYlBu_r, \
    #                levels = levels, extend = "both")
    cs1 = ax.pcolormesh(lon, lat, data, transform=ccrs.PlateCarree(), cmap = plt.cm.inferno, \
                     vmin = levels[0], vmax = levels[-1],)
    cbar1 = fig.colorbar(cs1, orientation = "horizontal", shrink = 0.7)
    cbar1.set_label("m/s", rotation = 0)
    # Add Title
    ax.set_title("Wind speed at 250hPa\n" + thisDate.strftime("%d %b %Y"))
    #ax.coastlines()
    plt.savefig("./figs/fig" + str(jt).zfill(5) + ".png")


    plt.close(fig)
