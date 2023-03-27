import numpy as np
import csv
import matplotlib.pyplot as plt
from scipy import stats
import matplotlib
matplotlib.rcParams['font.family'] = "Arial Narrow"

fileIn = "/Users/massonnetf/CLIMDATA//obs/atmos/gmst/Berkeley/Berkeley/raw//file.txt"

years = list()
gmst  = list()

with open(fileIn, mode = "r") as csvFile:
	csvReader = csv.reader(csvFile)
	[next(csvReader) for i in range(58)]
	for row in csvReader:
		print(row)
		years.append(int(row[0].split()[0]))
		gmst.append(float(row[0].split()[1]))
		


fig, ax = plt.subplots(1, 1, figsize = (6, 3))

# Center on 1850-1899
gmstRef = np.mean([d[1] for d in zip(years, gmst) if d[0] >= 1850 and d[0] <= 1899])
gmstAno= gmst - gmstRef



gmst2022 = [d[1] for d in zip(years, gmstAno) if d[0] == 2022][0]
gmstMax = np.max(gmstAno)

ax.plot(years, gmstAno, lw = 1, color = "lightblue")
ax.scatter(years, gmstAno, 2, marker = "s", color = "lightblue")
ax.set_title("Global mean surface temperature Anomalies relative to 1850-1899\nBerkeley Earth Data set. Value for 2022: " + str(np.round(gmst2022, 2)) + "°C")
ax.grid()
ax.set_ylabel("$^\circ$C")
ax.set_ylim(-0.5, 2.0)
ax.set_xlim(1850, 2040)

ax.xaxis.label.set_color('white')
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')
ax.spines['bottom'].set_color('white')
ax.spines['top'].set_color('white')
ax.spines['left'].set_color('white')
ax.spines['right'].set_color('white')

fig.savefig("./fig.png", dpi = 300, transparent = True)
