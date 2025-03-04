#!/usr/bin/python
# Francois Massonnet
# Nov 2022
# Analysis of spread in growth and melt seasons
# The data can be obtained at:
# ftp://sidads.colorado.edu/DATASETS/NOAA/G02135/north/daily/data/
# ftp://sidads.colorado.edu/DATASETS/NOAA/G02135/south/daily/data/
# Use the script getdata.bash to update the NSIDC data

import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
from datetime import timedelta

plt.close("all")
hemi = "SH"

filein = "/Users/massonnetf/CLIMDATA/obs/ice/siextents/NSIDC/seaiceindex/raw/s_seaice_extent_daily_v3.0.csv"
colax=(182.0/255, 219.0/255, 1.0)

j = 0

mydates = list()
extents = list()
mydata  = list()
with open(filein, 'r') as csvfile:
  obj = csv.reader(csvfile, delimiter = ',', skipinitialspace = True)
  nd = obj.line_num - 2 # nb data
  for row in obj:

    print(row)
    if j <= 1:
      print("ignore, header")
    elif len(row) == 6:
      extents.append(row[3])
      mydates.append(datetime.date(int(row[0]), int(row[1]), int(row[2])))
      mydata.append(( datetime.date(int(row[0]), int(row[1]), int(row[2])), \
                      float(row[3])))
    j = j + 1
      

yearmax = mydates[-1].year
yearmin = mydates[0].year
nyear   = yearmax - yearmin + 1



fig, ax = plt.subplots(1, 2, figsize = (12, 4))

# Growing season
for year in np.arange(1979, 2022):
  theseDates = [datetime.datetime(1904, m[0].month, m[0].day) for m in mydata if m[0].year == year and m[0].month >= 3 and m[0].month < 10]
  thisData    = [m[1] for m in mydata if m[0].year == year and m[0].month >= 3 and m[0].month < 10]

  # Center the data
  thisData = np.array(thisData) - thisData[0]

  ax[0].plot(theseDates, thisData)
  ax[0].xaxis.set_major_formatter(mdates.DateFormatter('%b'))

  ax[0].set_title("Growing season: extent relative to 1 Mar")
  ax[0].set_ylabel("Million km$^2$")
# Melting season
for year in np.arange(1979, 2021):
  theseDatesTmp = [datetime.datetime(1904, m[0].month, m[0].day) for m in mydata if m[0] >= datetime.date(year, 10, 1) and m[0] <= datetime.date(year + 1, 2, 28)]
  # Fix year issue
  theseDates = list()
  for t in theseDatesTmp:
    if t.month <= 2:
      theseDates.append(datetime.datetime(t.year + 1, t.month, t.day))
    else:
      theseDates.append(t)

  thisData = [m[1] for m in mydata if m[0] >= datetime.date(year, 10, 1) and m[0] <= datetime.date(year + 1, 2, 28)]

  # Center the data
  thisData = np.array(thisData) - thisData[0]

  ax[1].plot(theseDates, thisData)
  ax[1].xaxis.set_major_formatter(mdates.DateFormatter('%b'))
  ax[1].set_title("Melting season: extent relative to 1 Oct")
  ax[1].set_ylabel("Million km$^2$")
plt.savefig("./fig.png", dpi = 150)
