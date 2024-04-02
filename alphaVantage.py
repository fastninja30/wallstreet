from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
import numpy as np


ts = TimeSeries(key='apikeyALPHA.txt', output_format='json')


#monthly = ts.get_monthly('AAPL')






def plotWeekly():
    weekly = ts.get_weekly('AAPL')
    # Lists to store dates and prices
    xVal = []
    yVal_open = []
    yVal_close = []

    # Iterate through the dictionary to extract dates and prices
    for date, data_dict in weekly[0].items():
        xVal.append(date)
        open_price = data_dict.get('1. open')
        close_price = data_dict.get('4. close')
        if open_price:
            yVal_open.append(float(open_price))  # Convert to float for plotting
        if close_price:
            yVal_close.append(float(close_price))  # Convert to float for plotting

    # Plotting
    plt.plot(xVal, yVal_open, label="OPEN")
    plt.plot(xVal, yVal_close, label="CLOSE")

    # Adding labels and legend
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Weekly Open and Close Prices')
    plt.legend()
    # Rotate x-axis labels
    plt.xticks(rotation=45)

    # Adjusting figure size
    plt.gcf().set_size_inches(10, 6)
    # Set step size for x-axis tick marks
    step = max(1, len(xVal) // 10)  # Adjust the divisor as needed
    plt.xticks(np.arange(0, len(xVal), step), rotation=45)
    plt.show()


def plotDaily():
    daily = ts.get_daily('AAPL')
    # Lists to store dates and prices
    xVal = []
    yVal_open = []
    yVal_close = []

    # Iterate through the dictionary to extract dates and prices
    for date, data_dict in daily[0].items():
        xVal.append(date)
        open_price = data_dict.get('1. open')
        close_price = data_dict.get('4. close')
        if open_price:
            yVal_open.append(float(open_price))  # Convert to float for plotting
        if close_price:
            yVal_close.append(float(close_price))  # Convert to float for plotting

    # Plotting
    plt.plot(xVal, yVal_open, label="OPEN")
    plt.plot(xVal, yVal_close, label="CLOSE")

    # Adding labels and legend
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Daily Open and Close Prices')
    plt.legend()
    # Rotate x-axis labels
    plt.xticks(rotation=45)

    # Adjusting figure size
    plt.gcf().set_size_inches(10, 6)

    # Set step size for x-axis tick marks
    step = max(1, len(xVal) // 10)  # Adjust the divisor as needed
    plt.xticks(np.arange(0, len(xVal), step), rotation=45)
    plt.show()


plotWeekly()