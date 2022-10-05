import numpy as np
import matplotlib.pyplot as plt
import os
import cdsapi; c = cdsapi.Client()
from datetime import datetime, timedelta
import matplotlib.dates as mdates
from netCDF4 import Dataset

import matplotlib
matplotlib.rcParams['font.family'] = "Arial Narrow"

# Functions
def downloadERA5(year, listMonths, listDays, listTime, domainArea, outFile = "./data/download.nc"):
    
    c.retrieve(
        'reanalysis-era5-single-levels',
        {
        'product_type': 'reanalysis',
        'format'      : 'netcdf',
        'variable'    : '2m_temperature',
        'year'        : str(int(year)),
        'month'       : listMonths,
        'day'         : listDays,
        'time'        : listTime,
        'area'        : domainArea,
                    },
                    outFile)
                    
                    
# -- Editable parameters --

# ERA5 First date of data availability. Should not change
startDate    = datetime(1959, 1, 1) 
startYear    = startDate.year
# The lat max, lon min, lat min, lon max. For Brussels: [50.8, 4.2, 50.7, 4.3]
domainArea   = [50.8, 4.2, 50.7, 4.3]
dateRef = datetime(1900, 1, 1) # The origin time in ERA5

# Constants
offsetKtoC = -273.16

# Fetch information regarding today
today        = datetime.today()
currentYear  = today.year
currentDay   = today.day
currentMonth = today.month

# Define last day of data availability (imposed by ERA5)
endDate      = today + timedelta(days = - 7)
endYear      = endDate.year
endMonth     = endDate.month
endDay       = endDate.day
# Assemble input files. One file per year. Special attention to end year
# because files need to be downloaded separately for the last month
# (otherwise, crash)

# The reason it's done this way is (1) to not redownload everything
# and (2) because NetCDF format differs depending on how lumped the
# data is. I found that downloading month by month the last year
# does not cause those issues.

dates = list()
data  = list()

for year in np.arange(startYear, endYear):
	print(year)
	fileYear = "./data/download_T2M_" + str(year) + ".nc"
	if os.path.exists(fileYear):
		print("File " + fileYear + " exists, no download")
	else:
		print("Downloading")
		listMonths = [str(m).zfill(2) for m in np.arange(1, 12 + 1)]
		listDays   = [str(d).zfill(2) for d in np.arange(1, 31 + 1)]
		listTime   = [str(j).zfill(2) + ":00" for j in np.arange(24)]
		downloadERA5(year, listMonths, listDays, listTime, domainArea, outFile = fileYear)

	# Store the data
	f = Dataset(fileYear, mode = "r")
	thisData = np.squeeze(f.variables["t2m"][:]).data + offsetKtoC # .data to unmask
	thisTime = f.variables["time"][:]
	thisDate = [dateRef + timedelta(days = t / 24) for t in thisTime]
	f.close()


 	# Save the data in array
	[dates.append(d) for d in thisDate]
	[data.append(d)  for d in thisData]

# Treat the special case of the last year
# 1. Download all months until previous month

# If the month of the last available date is january, then we
# can download all days of that month
if endMonth == 1:
	listMonths = ['01']
	listDays   = [str(d).zfill(2) for d in np.arange(1, endDay + 1)]
	listTime   = [str(j).zfill(2) + ":00" for j in np.arange(24)]
	fileOut    = "./data/download_T2M_" + str(endYear) + "-" + str(endMonth).zfill(2) + ".nc"
	downloadERA5(endYear, listMonths, listDays, listTime, domainArea, outFile = fileOut)

	f = Dataset(fileOut, mode = "r")
	thisData = np.squeeze(f.variables["t2m"][:]).data + offsetKtoC # .data to unmask
	thisTime = f.variables["time"][:]
	thisDate = [dateRef + timedelta(days = t / 24) for t in thisTime]
	f.close()


 	# Save the data in array
	[dates.append(d) for d in thisDate]
	[data.append(d)  for d in thisData]
	
else:
	for m in np.arange(1, endMonth):
		listMonths = [str(m).zfill(2)]
		listDays   = [str(d).zfill(2) for d in np.arange(1, 31 + 1)]
		listTime   = [str(j).zfill(2) + ":00" for j in np.arange(24)]
		fileOut = "./data/download_T2M_" + str(endYear) + "_" + str(m).zfill(2) + ".nc"
		if os.path.exists(fileOut):
			print("File " + fileOut + " already exists, not downloading")
		else:
			downloadERA5(endYear, listMonths, listDays, listTime, domainArea, outFile = fileOut)

		# Read in the data
		f = Dataset(fileOut, mode = "r")
		thisData = np.squeeze(f.variables["t2m"][:]).data + offsetKtoC # .data to unmask
		thisTime = f.variables["time"][:]
		thisDate = [dateRef + timedelta(days = t / 24) for t in thisTime]
		f.close()
	 	# Save the data in array
		[dates.append(d) for d in thisDate]
		[data.append(d)  for d in thisData]
	
	# Download all days of current month
	listMonths = [str(endMonth).zfill(2)]
	listDays   = [str(d).zfill(2) for d in np.arange(1, endDay + 1)]
	listTime   = [str(j).zfill(2) + ":00" for j in np.arange(24)]
	fileOut = "./data/download_T2M_" + str(endYear) + "_" + str(endMonth).zfill(2) + ".nc"
	downloadERA5(endYear, listMonths, listDays, listTime, domainArea, outFile = fileOut)

	f = Dataset(fileOut, mode = "r")
	thisData = np.squeeze(f.variables["t2m"][:]).data + offsetKtoC # .data to unmask
	thisTime = f.variables["time"][:]
	thisDate = [dateRef + timedelta(days = t / 24) for t in thisTime]
	f.close()
 	# Save the data in array
	[dates.append(d) for d in thisDate]
	[data.append(d)  for d in thisData]
	


# Check that there is no issue in the date recording
if len(set([dates[j + 1] - dates[j] for j, d in enumerate(dates[:-1])])) != 1:
	stop()



# Remove the 29th of Februaries. Those are so annoying.
data  = [data[j] for j, d in enumerate(dates) if not (d.month == 2 and d.day == 29)]
dates = [d for d in dates if not (d.month == 2 and d.day == 29)]


yearbc, yearec = 1991, 2020 #startYear, endYear  # Years defining the climatology 

years = np.arange(startYear, endYear + 1)

# Data check plot
fig, ax = plt.subplots()
ax.plot(dates, data)
fig.savefig("./figs/check.png")
plt.close(fig)


# Make daily statistics
print("Making daily statistics")
datesDay = dates[::24]

print("... Mean")
dataDayMean =   [np.mean(data[j : j + 24]) for j in np.arange(0, len(data), 24)]
print("... Median")
dataDayMedian =   [np.mean(data[j : j + 24]) for j in np.arange(0, len(data), 24)]
print("... Max")
dataDayMax =   [np.max(data[j : j + 24]) for j in np.arange(0, len(data), 24)]
print("... Min")
dataDayMin =   [np.min(data[j : j + 24]) for j in np.arange(0, len(data), 24)]


# Data check plots
fig, ax = plt.subplots(2, 2)
ax[0, 0].plot(datesDay, dataDayMean) ; ax[0, 0].set_title("Day mean")
ax[0, 1].plot(datesDay, dataDayMedian); ax[0, 1].set_title("Day median")
ax[1, 0].plot(datesDay, dataDayMin);    ax[1, 0].set_title("Day min")
ax[1, 1].plot(datesDay, dataDayMax);    ax[1, 1].set_title("Day max")

fig.tight_layout()
fig.savefig("./figs/check2.png")

# Annual outlooks
for year in years:
	print("Annual outlook " + str(year))
	# Subset data
	subDates = [d for d in datesDay if d.year == year]
	subDataMean  = [dataDayMean[j] for j, d in enumerate(datesDay) if d.year == year]
	subDataMin  =  [dataDayMin[j] for j, d in enumerate(datesDay) if d.year == year]
	subDataMax  = [dataDayMax[j] for j, d in enumerate(datesDay) if d.year == year]
	fig, ax = plt.subplots(figsize = (8, 3))
	ax.plot(subDates, subDataMean, linestyle = "-", color = "black", label = "Day mean")
	ax.plot(subDates, subDataMin, linestyle = "-", linewidth = 1, color = "blue", label = "Day min.")
	ax.plot(subDates, subDataMax, linestyle = "-", linewidth = 1, color = "red", label = "Day max.")
	ax.grid()
	ax.set_ylabel("°C")
	ax.set_title("Daily temperature statistics")
	fig.savefig("./figs/outlook_" + str(year) + ".png")
	plt.close(fig)

# Make annual statistics
print("Making annual statistics")
print("... Mean")
dataYearMean = [np.mean([data[jj] for jj, dd in enumerate(dates) if dd.year == y]) for y in years]

# Data check plots
fig, ax = plt.subplots()
ax.plot(years, dataYearMean)
ax.grid()
ax.set_title("Warning: last year is not finished")
fig.savefig("./figs/check3.png")
plt.close(fig)



# Compute seasonal cycle
# Ref date (no leap)
print("... Computing annual cycle")
dateOneYear = [dateRef + j * timedelta(days = 1) for j in np.arange(365)]


cycle = [np.mean([dataDayMean[j] for j, dd in enumerate(datesDay) if \
		dd.day   == d.day    and \
		dd.month == d.month  and \
		dd.year >= yearbc    and \
		dd.year <= yearec        \
		]) for d in dateOneYear]
cycle = np.array(cycle)

# Smoothed cycle
print("... Smoothing & tiling cycle")
widthSmooth = 61
cycleSmoothed = [np.mean([cycle[k] for k in [(365 + d - j) % 365 for j in range(-int(widthSmooth / 2), int(widthSmooth / 2) + 1)]]) for d in np.arange(len(cycle))]
cycleSmoothedTiled = [cycleSmoothed[j % 365] for j in np.arange(len(datesDay))]

print("... Producing figures")
# Data check plots
fig, ax = plt.subplots()
ax.plot(dateOneYear, cycle)
ax.plot(dateOneYear, cycleSmoothed, "k--")
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
ax.grid()
ax.set_title("Annual cycle " + str(yearbc) + "-" + str(yearec))
fig.savefig("./figs/check4.png")
plt.close(fig)


# Plot previous 365 days
fig, ax = plt.subplots(figsize = (10, 4), dpi = 150)

# Tile the cycle
# Subset the data
#ax.plot(datesDay, dataDayMean, lw = 1, color = "k")
ax.plot(datesDay, cycleSmoothedTiled, lw = 1, color = "k", ls = "--", label = "Climatologie (" + str(yearbc) + "-" + str(yearec) + ")")

#ax.plot(dateOneYear, cycle_smoothed, "k--")
anomalies = np.array(dataDayMean) - np.array(cycleSmoothedTiled)
for j, d in enumerate(datesDay):
	if d > today - timedelta(days = 3 * 365):
		xmin, xmax = -10, 10
		color = plt.cm.RdBu_r(int((anomalies[j]- xmin) * 255 / (xmax - xmin)))[:3]
		ax.bar(datesDay[j], anomalies[j], bottom = cycleSmoothedTiled[j], color = color, lw = 2, width = 1.0)
ax.grid()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b %Y'))
ax.set_axisbelow(True)
ax.set_xlim(today - timedelta(days = 3 * 365), today + timedelta(days = 10))
ax.plot((-1e9, 1e9), (0, 0), color = "black")
ax.set_ylabel("$^\circ C$")
ax.set_title("Température journalière moyenne de l'air à 2 m, Bruxelles (données ERA5)")
ax.legend()
fig.tight_layout()
fig.savefig("./figs/last365.png")
plt.close(fig)



