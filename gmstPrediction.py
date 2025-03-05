import numpy as np
import csv
import matplotlib.pyplot as plt
from scipy import stats

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
		


fig, ax = plt.subplots(2, 1, figsize = (6, 6))

# Center on 1850-1899
gmstRef = np.mean([d[1] for d in zip(years, gmst) if d[0] >= 1850 and d[0] <= 1899])
gmstAno= gmst - gmstRef



gmst2022 = [d[1] for d in zip(years, gmstAno) if d[0] == 2022][0]
gmstMax = np.max(gmstAno)

ax[0].plot(years, gmstAno, lw = 1)
ax[0].scatter(years, gmstAno, 2, marker = "s")
ax[0].set_title("Global mean surface temperature Anomalies relative to 1850-1899\nBerkeley Earth Data set. Value for 2022: " + str(np.round(gmst2022, 2)) + "°C")
ax[0].grid()
ax[0].set_ylabel("$^\circ$C")
ax[0].set_ylim(-0.5, 2.0)
ax[0].set_xlim(1850, 2040)


# Lag studied:
lag = 1

# Training data
y2yDiff = gmstAno[(1970 - 1850) + lag:] - gmstAno[(1970 - 1850):-lag]

count, bins = np.histogram(y2yDiff, density = True, bins = np.arange(-0.5, 0.5, 0.01))
ax[1].set_title("Year-to-year differences")
# Fit PDF 
xpdf = np.linspace(-0.5, 0.5, 1000)
kernel = stats.gaussian_kde(y2yDiff)
pdf = kernel(xpdf).T
ax[1].bar(years[(1970 - 1850) + lag:], y2yDiff)
ax[1].set_xlim(1850, 2040)
ax[1].set_ylim(-0.5, 0.5)
ax[1].grid()
#ax[1].bar(bins[1:], count, width = 0.01)
#ax[1].plot(xpdf, pdf,)
plt.tight_layout()
plt.savefig("./fig.png", dpi = 300)




print("Probability that " + str(2022 + lag) + " breaks 1.5°C: ")
prob = np.sum(pdf[xpdf > (1.5 - gmst2022)]) / np.sum(pdf)
print(str(np.round(prob * 100.0)))

print("Probability that " + str(2022 + lag) + " breaks record: ")
prob = np.sum(pdf[xpdf > (gmstMax - gmst2022)]) / np.sum(pdf)
print(str(np.round(prob * 100.0)))

