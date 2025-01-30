from __future__ import print_function

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from pykalman import KalmanFilter

import yfinance as yf

def draw_date_coloured_scatterplot(etfs, prices):
    plen = len(prices)
    colour_map = plt.cm.get_cmap('YlOrRd')
    colours = np.linspace(0.1, 1, plen)

    scatterplot = plt.scatter(
        prices[etfs[0]], prices[etfs[1]],
        s=30, c=colours, cmap=colour_map,
        edgecolors='k', alpha=0.8
    )

    # Create a color-bar with formatted dates as tick labels
    colourbar = plt.colorbar(scatterplot)
    colourbar.ax.set_yticklabels(
        [str(p.date()) for p in prices[::plen // 9].index]
    )
    plt.xlabel(prices.columns[0])
    plt.ylabel(prices.columns[1])
    plt.show()

def calc_slope_intercept_kalman(etfs, prices):
    delta = 1e-5
    trans_cov = delta / (1 - delta) * np.eye(2)
    obs_mat = np.vstack([prices[etfs[0]], np.ones(prices[etfs[0]].shape)]).T[:, np.newaxis]

    kf = KalmanFilter(
        n_dim_obs=1,
        n_dim_state=2,
        initial_state_mean=np.zeros(2),
        initial_state_covariance=np.ones((2,2)),
        transition_matrices=np.eye(2),
        observation_matrices=obs_mat,
        observation_covariance=1.0,
        transition_covariance=trans_cov
    )

    state_means, state_covs = kf.filter(prices[etfs[1]].values)
    return state_means, state_covs

def draw_slope_intercept_changes(prices, state_means):
    pd.DataFrame(
        dict(
            slope=state_means[:, 0],
            intercept=state_means[:, 1]
        ), index=prices.index
    ).plot(subplots=True)

    plt.show()


if __name__ == "__main__":
    etfs =["TLT", "IEI"]
    start_date = "2010-08-01"
    end_date = "2016-08-01"

    etf_df1 = yf.download(etfs[0], start=start_date, end=end_date)
    etf_df2 = yf.download(etfs[1], start=start_date, end=end_date)

    print(etf_df1.head())
    print(etf_df2.head())

    prices = pd.DataFrame(index=etf_df1.index)
    prices[etfs[0]] = etf_df1["Close"]
    prices[etfs[1]] = etf_df2["Close"]

    draw_date_coloured_scatterplot(etfs, prices)

    state_means, state_covs = calc_slope_intercept_kalman(etfs, prices)

    draw_slope_intercept_changes(prices, state_means)
