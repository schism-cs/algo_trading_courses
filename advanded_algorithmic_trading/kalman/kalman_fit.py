from __future__ import print_function

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from pykalman import KalmanFilter

def draw_date_coloured_scatterplot(etfs, prices):
    plen = len(prices)
    colour_map = plt.cm.get_cmap('YlOrRd')
    colours = np.linspace(0.1, 1, plen)

    scatterplot = plt.scatter(
        prices[etfs[0]], prices[etfs[1]],
        s = 30, c=colours, cmap=colour_map,
        edgecolors='k', alpha=0.8
    )

    # Create a color-bar with formatted dates as tick labels
    colourbar = plt.colorbar(scatterplot)
    colourbar.ax.set_yticklabels(
        [str(p.date()) for p in prices[::plen//9].index]
    )
    plt.xlabel(prices.columns[0])
    plt.ylabel(prices.columns[1])
    plt.show()


