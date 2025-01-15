import numpy as np
import pandas as pd
import yfinance as yf
import seaborn as sns
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib import interactive

from datetime import datetime, timedelta

pd.set_option('display.max_columns', None)

if __name__ == '__main__':
    # DOWNLOAD DATA
    yesterday = datetime.now() - timedelta(1)
    yesterday_str = datetime.strftime(yesterday, "%Y-%m-%d")

    random_stocks_tickers = [
        "AAPL",  # Apple - Technology
        "MSFT",  # Microsoft - Technology
        "GOOGL",  # Alphabet - Technology
        "PLUG",  # Plug Power - Clean Energy
        "AMRC",  # Ameresco - Renewable Energy
        "TSLA",  # Tesla - Automotive/Energy
        "NKE",   # Nike - Apparel
        "CROX",  # Crocs - Consumer Goods
        "VRTX",  # Vertex Pharmaceuticals - Healthcare
        "UNH",  # UnitedHealth Group - Healthcare
        "TTWO",  # Take-Two Interactive - Gaming
        "TGT",  # Target - Retail
        "XOM",  # ExxonMobil - Energy
        "CPRT",  # Copart - Automotive Services
        "ATKR",  # Atkore - Industrial Products
        "DE",  # Deere & Co. - Agriculture/Industrial
        "LULU",  # Lululemon - Apparel
        "BILI",  # Bilibili - Entertainment/Tech (China)
        "BLNK",  # Blink Charging - Electric Vehicle Charging
        "CRWD"  # CrowdStrike - Cybersecurity
    ]

    stocks: DataFrame = yf.download(random_stocks_tickers,
                                    start="2020-01-01",
                                    end=yesterday_str,
                                    interval="1d")

    stocks_close = stocks.loc[:, "Close"]

    norm_close = stocks_close.div(stocks_close.iloc[0]).mul(100)
    norm_close.plot(title="Normalized Close", fontsize=12)

    first_non_null_indices = stocks_close.apply(lambda col: col.notna().idxmax() if col.notna().any() else None)

    print("Stock first available date:")
    print(first_non_null_indices)

    stocks_close = stocks_close.dropna()
    # stocks_close.plot(title="Close", fontsize=12)

    returns = stocks_close.pct_change().dropna()

    annual_summary = returns.describe().T.loc[:, ["mean", "std"]]
    annual_summary["mean"] = annual_summary["mean"] * 252
    annual_summary["std"] = annual_summary["std"] * np.sqrt(252)
    print(annual_summary.head(20))

    annual_summary.plot.scatter(x="std", y="mean", s=50, fontsize=12)
    for i in annual_summary.index:
        plt.annotate(i, xy=(annual_summary.loc[i, "std"] + 0.002, annual_summary.loc[i, "mean"] + 0.002), size=15)
    plt.xlabel("Annual risk (std)")
    plt.ylabel("Annual return")
    plt.title("Risk / Return")

    # COVARIANCE AND CORRELATION
    plt.figure(figsize=(12, 8))
    sns.heatmap(returns.corr(), cmap="Reds", annot=True, annot_kws={"size": 12})
    plt.title("Stock Correlation")

    # plt.figure(figsize=(12, 8))
    # sns.heatmap(returns.cov(), annot=True, cmap="coolwarm", fmt=".2f", cbar=True)
    # plt.title("Stock Covariance")

    risk_free_rate = 0.046  # 4.6% annualized

    # Compute Sharpe Ratio
    annual_summary["sharpe_ratio"] = (annual_summary["mean"] - risk_free_rate) / annual_summary["std"]

    # Sort the top 10 stocks by Sharpe Ratio
    sorted_stocks = annual_summary.sort_values(by="sharpe_ratio", ascending=False)

    # Initialize the filtered list with the stock having the highest Sharpe ratio
    filtered_stocks = [sorted_stocks.index[0]]

    # Set correlation threshold (e.g., 0.9 for highly correlated stocks)
    correlation_threshold = 0.5

    # Iterate over the sorted stocks (excluding the first one, which is already added)
    for stock in sorted_stocks.index[1:]:
        correlations = [
            returns[stock].corr(returns[existing_stock]) for existing_stock in filtered_stocks
        ]

        # Check if any correlation exceeds the threshold
        if all(abs(correlation) < correlation_threshold for correlation in correlations):
            # If no correlation is too high, add the stock to the filtered list
            filtered_stocks.append(stock)

        if len(filtered_stocks) == 5:
            break

    # Filter the original top_10_stocks DataFrame based on the selected uncorrelated stocks
    final_filtered_stocks = sorted_stocks.loc[filtered_stocks]

    # Display the final filtered stocks
    print(final_filtered_stocks)

    #plt.show()
