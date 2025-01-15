import datetime
import pprint

import arviz
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf
import pymc as pm
from pandas import DataFrame
from pymc.distributions.timeseries import GaussianRandomWalk
import seaborn as sns


def retrieve_price_dataframe(ticker, start_date, end_date):
    print(f"Downloading and plotting {ticker} log returns from {start_date} to {end_date}")
    data: DataFrame = yf.download(ticker, start=start_date, end=end_date)

    data["returns", ticker] = data["Close", ticker] / data["Close", ticker].shift(1)
    data["log_returns", ticker] = np.log(data["returns", ticker])

    data.dropna(inplace=True)

    return data


def plot_log_returns(data: DataFrame, ticker: str, column: str = "log_returns"):
    data[column, ticker].plot(linewidth=0.5)
    plt.ylabel(f"{ticker} daily log returns")
    plt.show()


def configure_stoch_volatility_model(log_returns):
    print("Configuring stochastic volatility model")

    model = pm.Model()
    with model:
        sigma = pm.Exponential("sigma", 50)
        nu = pm.Exponential("nu", 0.1)
        s = GaussianRandomWalk("s", sigma=sigma ** -2, shape=len(log_returns), init_dist=pm.Normal.dist(0, 100))
        logrets = pm.StudentT("logrets", nu, lam=pm.math.exp(-2.0 * s), observed=log_returns)

    return model


def fit_model(model: pm.Model, n_samples: int):
    print("Fitting the model")
    with model:
        trace = pm.sample(n_samples, chains=2)

    arviz.plot_trace(trace)
    plt.show()
    return trace


if __name__ == "__main__":
    ticker = "AMZN"
    stock_data = retrieve_price_dataframe(ticker, "2019-01-01", "2024-12-31")

    # plot_log_returns(stock_data, ticker)

    model = configure_stoch_volatility_model(stock_data["log_returns"])
    trace = fit_model(model, 500)

    print("Plotting the log volatility")
    k = 10
    opacity = 0.03
    plt.plot(trace.posterior["s"][0][::k].T, 'b', alpha=opacity)
    plt.xlabel("Time")
    plt.ylabel("Log volatility")
    plt.show()

    print("Plotting the absolute returns overlaid with volatility")
    plt.plot(np.abs(np.exp(stock_data["log_returns"])) - 1.0, linewidth=0.5)
    plt.plot(np.exp(trace.posterior["s"][0][::k].T), 'r', alpha=opacity)
    plt.xlabel("Trading Days")
    plt.ylabel("Absolute Returns / Volatility")
    plt.show()
