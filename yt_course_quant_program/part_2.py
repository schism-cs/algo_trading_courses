import numpy as np
import yfinance as yf
import pandas as pd
import seaborn as sns
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib import interactive

from datetime import datetime, timedelta

pd.options.mode.copy_on_write = True

if __name__ == '__main__':
    # DOWNLOAD DATA
    yesterday = datetime.now() - timedelta(1)
    yesterday_str = datetime.strftime(yesterday, "%Y-%m-%d")

    random_stocks_tickers = [
        "TSLA",
        "CRWD",
        "AAPL",
        "DE",
        "CROX",
        "SPY"
    ]

    stocks: DataFrame = yf.download(random_stocks_tickers,
                                    start="2020-01-01",
                                    end=yesterday_str,
                                    interval="1d")

    stocks_close = stocks.loc[:, "Close"].dropna()

    # SIMPLE AND LOG RETURNS
    simple_returns = stocks_close.pct_change().dropna()

    yearly_simple_returns = simple_returns.resample("YE").mean().mul(252)
    print(simple_returns)
    print(yearly_simple_returns)

    log_returns = np.log(stocks_close / stocks_close.shift(1)).dropna()
    yearly_log_returns = log_returns.resample("YE").mean().mul(252)
    print(log_returns)
    print(yearly_log_returns)

    # SMA and EMA
    for stock in random_stocks_tickers:
        stock_data: DataFrame = yf.download(stock, interval="1d")
        stock_close = stock_data["Close"]
        stock_close["ma50"] = stock_data["Close"].rolling(window=50).mean()
        stock_close["ma200"] = stock_data["Close"].rolling(window=200).mean()
        stock_close["ema100"] = stock_data["Close"].ewm(span=100).mean()
        stock_close["day"] = stock_close.index.day_name()
        stock_close["quarter"] = stock_close.index.quarter
        # stock_close.plot(title=stock)

        print(stock_close)

    # plt.show()
