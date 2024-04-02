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
    # closing values
    xVal1s = []

    for data_dict in daily[0].items():
        xVal1 = data_dict[0]
        if xVal1:
            xVal1s.append(xVal1)
    # List to store close prices
    yVal1s = []

    # Iterate through the dictionary to extract close prices for each date
    for data_dict in daily[0].items():
        yVal1 = data_dict[1].get('1. open')
        if yVal1:
            yVal1s.append(yVal1)

    plt.plot(xVal1s, yVal1s, label="OPEN")

    #closing values
    xVal2 = [key for key in daily[0].items()]
    # List to store close prices
    yVal2s = []

    # Iterate through the dictionary to extract close prices for each date
    for data_dict in daily[0].items():
        yVal2 = data_dict[1].get('4. close')
        if yVal2:
            yVal2s.append(yVal2)

    #plt.plot(xVal2, yVal2, label="CLOSE")

plotDaily()