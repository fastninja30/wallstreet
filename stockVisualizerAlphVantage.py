from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
import pandas as pd

class AlphaVantageData:
    def __init__(self, symbols, key):
        self.symbols = symbols
        self.key = key
        self.ts = TimeSeries(key=self.key, output_format='pandas')
        self.stocks = {}

    def get_data(self, start, end):
        for symbol in self.symbols:
            data, _ = self.ts.get_daily_adjusted(symbol=symbol, outputsize='full')
            self.stocks[symbol] = data.loc[start:end]

    def compute_returns_and_moving_averages(self):
        for symbol, data in self.stocks.items():
            data['Return'] = data['5. adjusted close'].pct_change()
            data['MA_50'] = data['5. adjusted close'].rolling(window=50).mean()
            data['MA_200'] = data['5. adjusted close'].rolling(window=200).mean()

    def visualize(self):
        fig, ax = plt.subplots(figsize=(14, 7))
        for symbol, data in self.stocks.items():
            ax.plot(data.index, data['5. adjusted close'], label=f'{symbol} Close')
            ax.plot(data.index, data['1. open'], label=f'{symbol} Open')
            ax.plot(data.index, data['MA_50'], label=f'{symbol} 50-day MA')
            ax.plot(data.index, data['MA_200'], label=f'{symbol} 200-day MA')
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: pd.to_datetime(x).strftime('%b %Y')))
        plt.title('Open and Closing prices with Moving Averages')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.grid(True)
        plt.legend()
        plt.show()

alpha_data = AlphaVantageData(['AAPL', 'GOOGL', 'MSFT'])
alpha_data.get_data('2020-01-01', '2022-12-31')
alpha_data.compute_returns_and_moving_averages()
alpha_data.visualize()
