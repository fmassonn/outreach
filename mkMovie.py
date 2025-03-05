import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from datetime import datetime, timedelta

def plot(file, variable = "z", level = 500):
    # Open the NetCDF file
    with nc.Dataset(file) as ds:
        # find time index length
        time_length = len(ds.dimensions['time'])
        for time_index in range(time_length):
            
            # Find the index corresponding to 500 millibars
            level_index = np.where(ds['level'][:] == level)[0]
            if len(level_index) == 0:
                raise ValueError(str(level) + " millibars level not found")
            level_index = level_index[0]
            
            # Read the geopotential data
            var = ds[variable][time_index, level_index, :, :]
            time_val = ds['time'][time_index]
            base_time = datetime.strptime(ds['time'].units, "hours since %Y-%m-%d %H:%M:%S.%f")
            time_stamp = base_time + timedelta(hours=int(time_val))
            print(time_stamp)
            
            # Get latitude and longitude values
            latitudes = ds['latitude'][:]
            longitudes = ds['longitude'][:]
            
            # Create a meshgrid for latitudes and longitudes
            lon, lat = np.meshgrid(longitudes, latitudes)
            
            # Create the plot with Orthographic projection centered over Europe
            fig, ax = plt.subplots(subplot_kw={'projection': ccrs.Orthographic(central_longitude=10, central_latitude=50)})
            
            # Set up map features
            ax.set_global()
            ax.coastlines(resolution='110m')
            ax.add_feature(cfeature.BORDERS, linestyle=':')
            ax.add_feature(cfeature.LAND, edgecolor='k')
            if variable == "z" and level == 500:
                levels = np.arange(48000, 59000 + 100, 1000)
                cmap = "tab20b"
            elif variable == "z" and level == 1000:
                levels = np.arange(-4000, 4000 + 100, 1000)
                cmap = "tab20b"
            elif variable == "t" and level == 500:
                levels = np.arange(230, 280, 2)
                cmap = "RdYlBu_r"
            elif variable == "t" and level == 1000:
                levels = np.arange(250, 300, 2)
                cmap = "RdYlBu_r"

            # Plot the geopotential data
            contour = ax.contourf(lon, lat, var, levels = levels, transform=ccrs.PlateCarree(), cmap=cmap, extend='both')
            # Add color bar
            plt.colorbar(contour, label=f'{ds[variable].long_name} ({ds[variable].units})', orientation='horizontal', fraction=0.05, pad=0.15)
            
            # Add title
            plt.title(f'{ds[variable].long_name} at {str(level)} millibars ('  + time_stamp.strftime("%d %b %Y  %H:%M") + ')')
    	
            plt.tight_layout()        
            # Save figure
            yyyymmddhhmm = time_stamp.strftime("%Y-%m-%d-%H%M")
            figName = 'figs/' + variable  + str(level) + "_" + yyyymmddhhmm + '.png'
            plt.savefig(figName)
            print(figName + " printed")
    
            plt.close()

## Example usage
for file in ["/Users/massonnetf/Downloads/81cdc12c7811ed1527ffb2c0b0688a0.nc"]:
    #file = "/cofast/fmasson/TMP/download_" + tag + ".nc"
    plot(file, variable = "z", level = 500)  # Replace 0 with the desired time index

