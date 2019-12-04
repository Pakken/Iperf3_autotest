# -*- coding: utf-8 -*-
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
from switches import create_topology
%matplotlib inline

# Point topology info
BOARDERS = int(input('Num of boarder leafs: '))
SPINES = int(input('Num of spines: '))
LEAFS = int(input('Num of leafs: '))

# Create figure and subplots
fig, axs = plt.subplots(1, 3, figsize=(12,3.7), dpi = 100)
fig.patch.set_facecolor('white')
fig.suptitle('Rates for {0} Boarders, {1} Spines, {2} Leafs and 10 Servers per Rack'.format(BOARDERS, SPINES, LEAFS))

# Create rates at the input edge of the DC
in_rates = np.arange(100,260, 10, dtype=int)
limits = [160, 40, 10]

# Create data for normal operation state
norm = (create_topology(in_rates,
                       boarder_spine_count = BOARDERS,
                       spine_count = SPINES,
                       leaf_count = LEAFS))

# Create data for half of spine dead case
osd = (create_topology(in_rates,
                      boarder_spine_count = BOARDERS,
                      spine_count = int(SPINES/2),
                      leaf_count = LEAFS))

# Create data for half of leafs dead
hld = (create_topology(in_rates,
                      boarder_spine_count = BOARDERS,
                      spine_count = SPINES,
                      leaf_count = int(LEAFS/2)))

# Create data for one spine three leafs
osd_hld = (create_topology(in_rates,
                      boarder_spine_count = 2,
                      spine_count = int(SPINES/2),
                      leaf_count = int(LEAFS/2)))

# Create titles for plots
for i in range(3):
    axs[i].plot(in_rates, [limits[i] for j in in_rates], 'k')
    axs[i].grid(True)
    axs[i].set_ylabel('Interface loading')
    axs[i].set_xlabel('Input rate')

axs[0].set_title('Boarder-Spine int')
axs[1].set_title('Spine-Leaf int')
axs[2].set_title('Leaf-Server int')

# Create plots for each state
for i, j, k in ((norm,'b', 'norm'),
                (osd, 'go', 'sp/2'),
                (hld, 'c*', 'le/2'),
                (osd_hld, '--r', 'sp&le/2')):
    axs[0].plot(in_rates, i[0] , j, label = k)
    axs[1].plot(in_rates, i[1] , j)
    axs[2].plot(in_rates, i[2], j)


fig.legend(loc = 'upper left')
fig.savefig('{0}_Br_{1}_sp_{2}_le.png'.format(BOARDERS, SPINES, LEAFS))
plt.show()