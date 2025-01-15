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
        "AAPL"
    ]

    stocks: DataFrame = yf.download(random_stocks_tickers,
                                    interval="1d")

    stocks_close = stocks.loc[:, "Close"].dropna()
    stocks_close["daily_returns"] = np.log(stocks_close["AAPL"].div(stocks_close["AAPL"].shift(1)))
    stocks_close.dropna(inplace=True)
    stocks_close["cumulative_returns"] = stocks_close["daily_returns"].cumsum().apply(np.exp)

    # DRAWDOWNS
    stocks_close["cumulative_max"] = stocks_close["cumulative_returns"].cummax()

    stocks_close[["cumulative_returns", "cumulative_max"]].plot()

    stocks_close["absolute_drawdown"] = stocks_close["cumulative_max"] - stocks_close["cumulative_returns"]
    stocks_close["perc_drawdown"] = (stocks_close["cumulative_max"] - stocks_close["cumulative_returns"])/stocks_close["cumulative_max"]
    print(stocks_close)

    print(stocks_close["perc_drawdown"].max())
    print(stocks_close["perc_drawdown"].idxmax())
    print(stocks_close.loc[(stocks_close.index <= stocks_close["perc_drawdown"].idxmax())])
    plt.show()
