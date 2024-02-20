import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import pandas_ta as ta
import backtrader as bt
import backtrader.analyzers as btanalyzers
import backtrader.feeds as btfeeds
import backtrader.strategies as btstrats
# from IPython.display import display
import datetime
curr=str(datetime.datetime.now())
date=curr[:10]
print("aaj ka date",date)
# DOW_30_TICKER=['AXP','AAPL', 'AMGN','MSFT', 'JPM']
# for index in DOW_30_TICKER:
#     aapl = yf.Ticker(index)
#     df = aapl.history(start="2024-1-1", end=date, interval="1d")
#     df.head()
#
#     # Let's compute the 5-d, 15-d and 25-d SMA for visualization
#     df["5d_sma_price"] = df['Close'].rolling(5).mean()
#     df["15d_sma_price"] = df['Close'].rolling(15).mean()
#     df["25d_sma_price"] = df['Close'].rolling(25).mean()
#
#     # The 25-d SMA for trading volume
#     df["25d_sma_volume"] = df['Volume'].rolling(25).mean()
#     df = df[df["25d_sma_price"].notna()]
#     print(df.head())
#     plt.figure(figsize=(12, 6))
#     plt.plot(df['Close'], color='blue', linewidth=0.5, label='Closing price')
#     plt.plot(df['5d_sma_price'], color='black', linewidth=0.5, label='5-d SMA')
#     plt.plot(df['15d_sma_price'], color='green', linewidth=0.5, label='15-d SMA')
#     plt.plot(df['25d_sma_price'], color='red', linewidth=0.5, label='25-d SMA')
#     plt.title("5-d, 15-d & 25-d SMA of {} closing prices".format(index))
#     plt.legend(loc='best')
#     plt.grid()
#     plt.show()
#
#
#
import matplotlib.pyplot as plt
import yfinance as yf

DOW_30_TICKER = ['AXP', 'AAPL', 'AMGN', 'MSFT', 'JPM']

# Calculate the number of rows and columns needed for the grid layout
num_rows = 3
num_cols = 2
total_subplots = num_rows * num_cols

# Create a figure and subplots
fig, axs = plt.subplots(num_rows, num_cols, figsize=(15, 10))
fig.tight_layout(pad=5.0)

# Flatten the axs array for easy iteration
axs = axs.flatten()

for index, ticker in enumerate(DOW_30_TICKER):
    aapl = yf.Ticker(ticker)
    df = aapl.history(start="2024-1-1", end=date, interval="1d")

    # Calculate SMA
    df["5d_sma_price"] = df['Close'].rolling(5).mean()
    df["15d_sma_price"] = df['Close'].rolling(15).mean()
    df["25d_sma_price"] = df['Close'].rolling(25).mean()

    # Filter out NaN values
    df = df[df["25d_sma_price"].notna()]

    # Plot SMA
    axs[index].plot(df.index.strftime('%m-%d'), df['Close'], color='blue', linewidth=0.5, label='Closing price')
    axs[index].plot(df.index.strftime('%m-%d'), df['5d_sma_price'], color='black', linewidth=0.5, label='5-d SMA')
    axs[index].plot(df.index.strftime('%m-%d'), df['15d_sma_price'], color='green', linewidth=0.5, label='15-d SMA')
    axs[index].plot(df.index.strftime('%m-%d'), df['25d_sma_price'], color='red', linewidth=0.5, label='25-d SMA')
    axs[index].set_title("5-d, 15-d & 25-d SMA of {} closing prices".format(ticker))
    axs[index].legend(loc='best')
    axs[index].grid()

    # axs[index].set_xticks(df.index.strftime('%m-%d'))
    # axs[index].set_xticklabels(df.index.strftime('%d'), rotation=45)
    # axs[index].tick_params(axis='x', rotation=45)

# Remove any unused subplots
for i in range(len(DOW_30_TICKER), total_subplots):
    fig.delaxes(axs[i])

# Show the plot
plt.show()
