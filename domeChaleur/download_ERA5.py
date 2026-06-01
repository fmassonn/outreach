#!/opt/anaconda3/bin/python3
import cdsapi
import sys

dataset = "reanalysis-era5-pressure-levels"
request = {
    "product_type": ["reanalysis"],
    "variable": [
        "geopotential",
#        "u_component_of_wind",
#        "v_component_of_wind",
#	"temperature",
    ],
    "year": ["2026"],
    "month": ["05"],
    "day": [str(i).zfill(2) for i in range(1, 31 + 1)],
    "time": [str(i).zfill(2) + ":00" for i in range(0, 24)],
    "pressure_level": ["500",],
    "data_format": "netcdf",
    "download_format": "unarchived",
#    "area": [50.5,-180, 50.5, 180] # up left down right
}

outfile = "./download.nc"

client = cdsapi.Client()
client.retrieve(dataset, request, outfile)

