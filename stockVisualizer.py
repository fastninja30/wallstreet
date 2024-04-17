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

    def calculate_daily_returns(self):
        for ticker, data in self.data.items():
            if data is not None:
                data['Daily_Return'] = data['Close'].pct_change()

    def add_moving_averages(self):
        for ticker, data in self.data.items():
            if data is not None:
                data['50-day_MA'] = data['Close'].rolling(window=50).mean()
                data['200-day_MA'] = data['Close'].rolling(window=200).mean()
    
    def plot_data(self):
        fig, ax = plt.subplots(figsize=(14, 7))
        for ticker, data in self.data.items():
            if data is not None:
                ax.plot(data.index, data['Close'], label=f'{ticker} Close')
                ax.plot(data.index, data['Open'], label=f'{ticker} Open')
                ax.plot(data.index, data['50-day_MA'], label=f'{ticker} 50-day MA')
                ax.plot(data.index, data['200-day_MA'], label=f'{ticker} 200-day MA')
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        plt.title('Open and Closing prices with Moving Averages')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.grid(True)
        plt.legend()
        plt.show()

stocks = StockData(['AAPL', 'GOOGL', 'MSFT'])
stocks.fetch_data('2020-01-01', '2022-12-31')
stocks.calculate_daily_returns()
stocks.add_moving_averages()
stocks.plot_data()
