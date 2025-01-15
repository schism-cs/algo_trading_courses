import numpy as np
import yfinance as yf
import pandas as pd
import seaborn as sns
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib import interactive

from datetime import datetime, timedelta

pd.options.mode.copy_on_write = True
pd.set_option('display.max_columns', None)


def test_strategy(stock, start, end, SMA):
    data = yf.download(stock, start=start, end=end)
    print(data)

    data["returns"] = np.log(data["Close"].div(data["Close"].shift(1)))
    data["SMA_S"] = data["Close"].rolling(int(SMA[0])).mean()
    data["SMA_L"] = data["Close"].rolling(int(SMA[1])).mean()
    data.dropna(inplace=True)

    data["position"] = np.where(data["SMA_S"] > data["SMA_L"], 1, -1)
    data["strategy"] = data["returns"] * data["position"].shift(1)
    data.dropna(inplace=True)

    absolute_returns = np.exp(data["strategy"].sum())
    std = data["strategy"].std() * np.sqrt(252)

    return absolute_returns, std


if __name__ == "__main__":
    print(test_strategy("MSFT", "2000-01-01", "2020-01-01", (50, 200)))
    print(test_strategy("AAPL", "2000-01-01", "2020-01-01", (50, 200)))
    print(test_strategy("TSLA", "2000-01-01", "2020-01-01", (50, 200)))
    print(test_strategy("SPY", "2000-01-01", "2020-01-01", (50, 200)))
