from datetime import date

import cdsapi
import numpy as np
c = cdsapi.Client()


doDownload = True

firstYear   = 1959  # in ERA5
currentYear = date.today().year
currentMonth= date.today().month
currentDay  = date.today().day

lagDays = 7 # Nb days it take for ERA5 to deliver current day

for year in np.arange(firstYear, currentYear + 1):
	if year != currentYear:
		listMonths = [str(m).zfill(2) for m in np.arange(1, 12 + 1)]
		listDays   = [str(d).zfill(2) for d in np.arange(1, 31 + 1)]
	else:
		listMonths = [str(m).zfill(2) for m in np.arange(1, currentMonth + 1)]
		listDays   = [str(d).zfill(2) for d in np.arange(1, currentDay + 1 - lagDays)]		
	if (year != currentYear and doDownload) or (year == currentYear):
		print("Doing " + str(int(year)))
		c.retrieve(
		    'reanalysis-era5-single-levels',
		    {
			'product_type': 'reanalysis',
			'format': 'grib',
			'variable': '2m_temperature',
			'year': str(int(year)),
			'month': listMonths,
			'day': listDays,
			'time': [
			    '00:00', '01:00', '02:00',
			    '03:00', '04:00', '05:00',
			    '06:00', '07:00', '08:00',
			    '09:00', '10:00', '11:00',
			    '12:00', '13:00', '14:00',
			    '15:00', '16:00', '17:00',
			    '18:00', '19:00', '20:00',
			    '21:00', '22:00', '23:00',
			],
			'area': [
			    50.8, 4.2, 50.7,
			    4.3,
			],
			'format': 'netcdf',
		    },
		    './data/download_T2M_' + str(year) + '.nc')


		
