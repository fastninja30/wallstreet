from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt


ts = TimeSeries(key='apikeyALPHA.txt', output_format='json')
daily = ts.get_daily('AAPL')
#weekly = ts.get_weekly('AAPL')
#monthly = ts.get_monthly('AAPL')

#print(daily[0].get("2024-03-25"))
print(daily)
#print(weekly[0])


def getMonthlyHigh():
    return None

def getMonthlyLow():
    return None





def plotDaily():
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
    # Adjusting x-axis margins (10% margin on each side)
    plt.margins(x=.04)
    plt.show()


plotDaily()