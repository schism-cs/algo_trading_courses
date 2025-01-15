import numpy as np
import yfinance as yf
import seaborn as sns
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib import interactive

from datetime import datetime, timedelta

if __name__ == '__main__':
    # DOWNLOAD DATA
    yesterday = datetime.now() - timedelta(1)
    yesterday_str = datetime.strftime(yesterday, "%Y-%m-%d")

    stocks: DataFrame = yf.download(["AAPL", "TSLA", "NVDA", "KO", "SPY"], start="2010-07-01", end=yesterday_str,
                                    interval="1d")

    print(stocks.tail(10))
    print()

    # EXTRACT CLOSING PRICES AND NORMALIZE
    close = stocks.loc[:, "Close"]
    close.plot(title="Close", fontsize=12)
    interactive(True)

    norm_close = close.div(close.iloc[0]).mul(100)
    norm_close.plot(title="Normalized Close", fontsize=12)

    # COMPUTE DAILY DIFFERENCE AND PERCENTAGE CHANGE
    aapl_close = close["AAPL"].copy().to_frame()
    aapl_close["Daily Diff"] = aapl_close["AAPL"].diff(periods=1)
    aapl_close["Daily % Change"] = aapl_close["AAPL"].pct_change(periods=1).mul(100)
    print(aapl_close)

    # RESAMPLING TIME SERIES
    aapl_close["AAPL"].resample("BME").last()  # Take the last value in each bin (supports also other operations)

    # COMPUTE DAILY RISK AND RETURNS
    returns = aapl_close["AAPL"].pct_change().dropna()
    print(returns.head(5))
    plt.figure()
    returns.plot(kind="hist", bins=100, title="AAPL returns")

    daily_mean_returns = returns.mean()
    daily_variance = returns.var()
    daily_standard_dev = returns.std()
    annual_mean_return = daily_mean_returns * 252

    print(f"Daily Returns >>> Mean: {daily_mean_returns} | Var: {daily_variance} | STD: {daily_standard_dev}")
    print(f"Annual Returns >>> Mean: {annual_mean_return}")

    # COMPUTE ANNUAL RISK AND RETURNS
    returns = close.pct_change().dropna()
    print(returns.head())

    annual_summary = returns.describe().T.loc[:, ["mean", "std"]]
    annual_summary["mean"] = annual_summary["mean"] * 252
    annual_summary["std"] = annual_summary["std"] * np.sqrt(252)
    print(annual_summary.head())

    annual_summary.plot.scatter(x="std", y="mean", s=50, fontsize=15)
    for i in annual_summary.index:
        plt.annotate(i, xy=(annual_summary.loc[i, "std"] + 0.002, annual_summary.loc[i, "mean"] + 0.002), size=15)
    plt.xlabel("Annual risk (std)")
    plt.ylabel("Annual return")
    plt.title("Risk / Return")

    # COVARIANCE AND CORRELATION
    plt.figure(figsize=(12, 8))
    sns.set(font_scale=1.4)
    sns.heatmap(returns.corr(), cmap="Reds", annot=True, annot_kws={"size": 15})

    interactive(False)
    plt.show()

