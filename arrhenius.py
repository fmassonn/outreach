import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.family'] = "Arial Narrow"
# Arrhenius prediction of temperature response to CO2
#Table VII
#Arrhenius, S. (1896). On the influence of carbonic acid in the air upon the temperature of the ground. The London, Edinburgh, and Dublin Philosophical Magazine and Journal of Science, 41(251), 237–276. https://doi.org/10.1080/14786449608620846

# Each row is a latitude. The fields are annual means for various "K" factors

latitudes = np.array([70, 60, 50, 40, 30, 20, 10, 0, -10, -20, -30, -40])
kFactor   = np.array([0.67, 1.5, 2.0, 2.5, 3.0])

data = np.array(\
[
[-3.1,	3.52,	6.05,	7.95,	9.3	],
[-3.22,	3.62,	6.02,	7.87,	9.3	],
[-3.3,	3.65,	5.92,	7.7,	9.17	],
[-3.32,	3.52,	5.7,	7.42,	8.82	],
[-3.17,	3.47,	5.3,	6.87,	8.1	],
[-3.07,	3.25,	5.02,	6.52,	7.52	],
[-3.02,	3.15,	4.95,	6.42,	7.3	],
[-3.02,	3.15,	4.95,	6.5,	7.35	],
[-3.12,	3.2,	5.07,	6.65,	7.62	],
[-3.2,	3.27,	5.35,	6.87,	8.22	],
[-3.35,	3.52,	5.62,	7.32,	8.8	],
[-3.37,	3.7,	5.95,	7.85,	9.25	],
]
)

colors = ["#1898e0", "#00b2ed", "#00bb62", \
               "#8bcd45", "#dbe622", "#f9c410", \
               "#f89e13", "#fb4c27", "#fb4865", \
               "#d24493", "#8f57bf", "#645ccc",]

fig, ax = plt.subplots(1, 1, figsize = (4, 3))

for j, l in enumerate(latitudes):
	ax.plot(kFactor, data[j, :], linestyle = "-", marker = "s", color = colors[j], lw = 1, ms = 2)
	#ax.text(kFactor[-1] + 0.1 + j / 10, data[j, -1], str(l), va = "center", ha = "left", fontsize = 8, )

ax.plot((kFactor[0], kFactor[-1]), (0, 0), lw = 0.5, color = [1, 1, 1])
ax.plot((1, 1), (-3, 10), lw = 0.5, color = [1, 1, 1])

ax.set_ylabel("$^\circ$ C", color = "white")
ax.set_xlim(0.5, 3.5)

ax.xaxis.label.set_color('white')
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')
ax.spines['bottom'].set_color('white')
ax.spines['top'].set_color('white')
ax.spines['left'].set_color('white')
ax.spines['right'].set_color('white')
fig.savefig("./fig.png", dpi = 300, transparent = True)

