import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class StockData:
    def __init__(self, tickers):
        self.tickers = tickers
        self.data = {}

    def fetch_data(self, start_date, end_date):
        for ticker in self.tickers:
            self.data[ticker] = yf.download(ticker, start=start_date, end=end_date)

    def plot_data(self):
        fig, ax = plt.subplots(figsize=(14, 7))
        for ticker, data in self.data.items():
            if data is not None:
                ax.plot(data.index, data['Close'], label=f'{ticker} Close')
                ax.plot(data.index, data['Open'], label=f'{ticker} Open')
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        plt.title('Open and Closing prices')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.grid(True)
        plt.legend()
        plt.show()

stocks = StockData(['AAPL', 'GOOGL', 'MSFT'])
stocks.fetch_data('2020-01-01', '2022-12-31')
stocks.plot_data()
