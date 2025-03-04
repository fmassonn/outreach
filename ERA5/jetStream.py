import matplotlib.pyplot as plt
import numpy as np

import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.util import add_cyclic_point
from netCDF4 import Dataset
import datetime
from datetime import timedelta

refDateNetcdf = datetime.datetime(1900, 1, 1)


f = Dataset("./data/download_UVP250hPa_2012.nc", mode = "r")
u = f.variables["u"][:]
v = f.variables["v"][:]
lon=f.variables["longitude"][:]
lat=f.variables["latitude"][:]
t  =f.variables["time"][:]
f.close()

f = Dataset("./data/download_T850hPa_2012.nc", mode = "r")
T = f.variables["t"][:] - 273.15
f.close()

s = np.sqrt(u ** 2 + v ** 2)


for jt in np.arange(0, len(t), 1):
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
    dataU= np.squeeze(u[jt,:,:])
    dataV= np.squeeze(v[jt,:,:])

    data[data < 30.0] = np.nan # Mask out slow points
    dataU[data < 30.0] = np.nan # Mask out slow points
    dataV[data < 30.0] = np.nan # Mask out slow points
    
    data, lon_tmp = add_cyclic_point(data, coord = lon)
    dataU, _      = add_cyclic_point(dataU, coord = lon)
    dataV, _      = add_cyclic_point(dataV, coord = lon)

    temp = np.squeeze(T[jt,:,:])
    temp, _       = add_cyclic_point(temp, coord = lon)
    # SST
    levels = np.arange(20, 60, step = 1.0)
    #levels = np.array([-2.0 + 0.1 * j for j in range(40)] + [2.0 + 0.5 * j for j in range(20)])
    #cs1 = ax.contourf(lon, lat, data,
    #            transform=ccrs.PlateCarree(),cmap = plt.cm.RdYlBu_r, \
    #                levels = levels, extend = "both")
    #cs1 = ax.pcolormesh(lon_tmp, lat, data, transform=ccrs.PlateCarree(), cmap = plt.cm.inferno, \
    #                 vmin = levels[0], vmax = levels[-1],)
    #cbar1 = fig.colorbar(cs1, orientation = "horizontal", shrink = 0.7)
    #cbar1.set_label("m/s", rotation = 0)

    # Temps
    cs2 = ax.pcolormesh(lon_tmp, lat, temp, transform=ccrs.PlateCarree(), cmap = plt.cm.RdYlBu_r, \
                     vmin = -10, vmax = 10,)

    cs1 = ax.pcolormesh(lon_tmp, lat, data, transform=ccrs.PlateCarree(), cmap = plt.cm.gist_gray_r, \
                     vmin = levels[0], vmax = levels[-1], alpha = 0.5)

    #LON_TMP, LAT = np.meshgrid(lon_tmp, lat)

    #dX  = dataU
    #dY  = dataV
    #norm = np.sqrt(dataU ** 2 + dataV ** 2)
    #dX /= norm
    #dY /= norm

    #cs3 = ax.plot((LON_TMP, LON_TMP+dX), (LAT, LAT + dY), transform=ccrs.PlateCarree())
    #step=4
    #cs3 = ax.quiver(LON_TMP[::step, ::step], LAT[::step,::step], dX[::step,::step], dY[::step,::step], transform=ccrs.PlateCarree())

    # Add Title
    ax.set_title("Atmospheric flow\n" + thisDate.strftime("%d %b %Y"))
    ax.coastlines(color = "black", resolution = "50m", lw = 1)
    plt.savefig("./figs/fig_2012_" + str(jt).zfill(5) + ".png")


    plt.close(fig)
