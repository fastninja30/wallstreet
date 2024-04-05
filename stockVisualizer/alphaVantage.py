from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
import numpy as np
import json

with open('../Credentials.json', 'r') as file:
    credentials = json.load(file)
api = credentials["alpha-vantage"]["api"]

ts = TimeSeries(key=api, output_format='json')



def getDayData(date, symbol):
    try:
        daily = ts.get_daily(symbol)
        # Check if the date is available in the data
        if date in daily[0]:
            # Get the data for the specified date
            data_for_date = daily[0][date]
            # Extract open and close prices
            open_price = data_for_date['1. open']
            close_price = data_for_date['4. close']
            return open_price, close_price
        else:
            return None, None  # Return None if the date is not available
    except Exception as e:
        print(f"Failed to get data: {e}")

def plotMonthly(symbol):
    try:
        monthly = ts.get_monthly(symbol)
        # Lists to store dates and prices
        xVal = []
        yVal_open = []
        yVal_close = []

        # Iterate through the dictionary to extract dates and prices
        for date, data_dict in monthly[0].items():
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
        plt.title('Monthly Open and Close Prices')
        plt.legend()
        # Rotate x-axis labels
        plt.xticks(rotation=45)

        # Adjusting figure size
        plt.gcf().set_size_inches(10, 6)
        # Set step size for x-axis tick marks
        step = max(1, len(xVal) // 10)  # Adjust the divisor as needed
        plt.xticks(np.arange(0, len(xVal), step), rotation=45)
        plt.show()
    except Exception as e:
        print(f"Failed to plot data: {e}")


def plotWeekly(symbol):
    try:
        weekly = ts.get_weekly(symbol)
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
    except Exception as e:
        print(f"Failed to plot data: {e}")


def plotDaily(symbol):
    try:
        daily = ts.get_daily(symbol)
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
    except Exception as e:
        print(f"Failed to plot data: {e}")


plotMonthly("GME")