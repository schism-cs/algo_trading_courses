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


if __name__ == '__main__':
    # DOWNLOAD DATA
    yesterday = datetime.now() - timedelta(1)
    yesterday_str = datetime.strftime(yesterday, "%Y-%m-%d")

    stocks: DataFrame = yf.download("AAPL", start="1991-01-01", interval="1d")

    # FIRST BASIC STRATEGY
    data = stocks["Close"]

    sma_slow = 100
    sma_fast = 50

    data["sma_fast"] = data["AAPL"].rolling(sma_fast).mean()
    data["sma_slow"] = data["AAPL"].rolling(sma_slow).mean()

    data = data.dropna()
    # BASIC STRATEGY -> SMA_FAST > SMA_SLOW --> LONG // SMA_FAST <= SMA_SLOW --> SHORT
    data["position"] = np.where(data["sma_fast"] > data["sma_slow"], 1, -1)

    data.loc["2016", ["sma_slow", "sma_fast", "position"]].plot(figsize=(12, 8),
                                                                title=F"AAPL - SMA{sma_fast} | SMA{sma_slow}",
                                                                secondary_y="position")

    data["returns_buy_hold"] = np.log(data["AAPL"].div(data["AAPL"].shift(1)))
    data["returns_strategy"] = data["returns_buy_hold"] * data.position.shift(1)
    data.dropna(inplace=True)
    print(data)

    # ADJUST STRATEGY, REMOVE SHORTS
    data["position_2"] = np.where(data["sma_fast"] > data["sma_slow"], 1, 0)
    data["returns_strategy_2"] = data["returns_buy_hold"] * data["position_2"].shift(1)
    data.dropna(inplace=True)

    # Compare strategy performance with classic buy and hold
    print("===== STRATEGY COMPARISON")
    print(data[["returns_buy_hold", "returns_strategy", "returns_strategy_2"]].sum())
    print()

    print("===== Return on 1$ investment")
    print(data[["returns_buy_hold", "returns_strategy", "returns_strategy_2"]].sum().apply(np.exp))  # 1$ investment will be now
    print()

    print("===== Annual STD")
    print(data[["returns_buy_hold", "returns_strategy", "returns_strategy_2"]].std() * np.sqrt(252))
    print()

    # DRAWDOWNS
    print("===== CUMULATIVE RETURNS =====")
    data[["cumret_buy_hold", "cumret_strategy", "cumret_strategy_2"]] = data[["returns_buy_hold", "returns_strategy", "returns_strategy_2"]].cumsum().apply(np.exp)
    print(data[["cumret_buy_hold", "cumret_strategy", "cumret_strategy_2"]])
    print()

    print("===== CUMULATIVE MAX RETURNS =====")
    data[["cummax_buy_hold", "cummax_strategy", "cummax_strategy_2"]] = data[["cumret_buy_hold", "cumret_strategy", "cumret_strategy_2"]].cummax()
    print(data[["cummax_buy_hold", "cummax_strategy", "cummax_strategy_2"]])
    print()

    asd = (data["cummax_buy_hold"] - data["cumret_buy_hold"]) / data["cummax_buy_hold"]
    print(f"Max DD B&H: {asd.max()}")

    asd = (data["cummax_strategy"] - data["cumret_strategy"]) / data["cummax_strategy"]
    print(f"Max DD Strategy: {asd.max()}")
    print(f"{asd.idxmax()}")
    max_idx = asd.idxmax()
    print(data.loc[(data.index <= max_idx) & (data.index >= max_idx - pd.Timedelta(days=5))])

    asd = (data["cummax_strategy_2"] - data["cumret_strategy_2"]) / data["cummax_strategy_2"]
    print(f"Max DD Strategy 2: {asd.max()}")