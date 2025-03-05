import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import csv
from scipy import interpolate
matplotlib.rcParams['font.family'] = "Arial Narrow"


h = 6.62607015e-34 # Planck constant
c = 299792458.0    # Light speed
lam= 2 ** np.linspace(1, 4.5, 100000) * 1e-6 # Wavelength in micrometers
kb = 1.380649e-23 # Boltzman constant

def blackBody(lam, T):
	return 2 * h * c ** 2 / lam ** 5 * 1 / ( np.exp(h * c / (lam * kb * T))-  1)



TEarth = 286.0

fig, axes = plt.subplots(2, 1, figsize = (4, 3))

ax = axes[0]
ax.plot(1e6 * lam, 1e-6 * blackBody(lam, TEarth), color = "white")


ax.set_ylabel("W.sr$^{-1}$.m$^{-2}$.$\mu$m$^{-1}$", color = "white")
ax.set_title("Irradiance spectrale à T = 13°C", color = "white")
#ax.set_xlabel("Longueur d'onde [$\mu$m]", color = "white")

# Read absorptivity data
csvReader = csv.reader(open("./data/Absorptivity_CO2.csv"), delimiter = ";")
next(csvReader); next(csvReader)
wl = list()
ab = list()
for jrow, row in enumerate(csvReader):
	wl.append(float(row[0]) / 1e6) # Convert to m
	ab.append(float(row[1]) )  #

interp = interpolate.interp1d(np.array(wl), np.array(ab), kind = "linear", \
                                  bounds_error = False)
interpAbsorpt = interp(lam)

ax = axes[1]
ax.plot(1e6 * lam, interpAbsorpt, lw = 1)
ax.set_title("Absorptivité du CO$_2$", color = "white")
#ax.set_xlim(0.5, 3.5)
ax.set_xlabel("Longueur d'onde [$\mu$m]", color = "white")

for ax in axes.flatten():
	ax.xaxis.label.set_color('white')
	ax.tick_params(axis='x', colors='white')
	ax.tick_params(axis='y', colors='white')
	ax.spines['bottom'].set_color('white')
	ax.spines['top'].set_color('white')
	ax.spines['left'].set_color('white')
	ax.spines['right'].set_color('white')

fig.tight_layout()
fig.savefig("./fig.png", dpi = 300, transparent = True)

