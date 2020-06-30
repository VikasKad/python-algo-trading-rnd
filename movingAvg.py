import pandas as pd
import matplotlib.pyplot as plt
import quandl

auth_token = 'BeMNC6TmXXVDzfsq7Ksa'
quandl.ApiConfig.api_key = auth_token


def SMA(data, nDays):
    # SMA = pd.Series(pd.rolling_mean(data['Close'], n), name='SMA')
    SMA = pd.Series(data['Close'].rolling(n).mean(), name='SMA')
    data = data.join(SMA)
    return data


data = pd.read_csv('titan.csv', parse_dates=True, index_col=0)

print('data', data)
data = pd.DataFrame(data)

n = 10
SMG = SMA(data, n)
SMA = SMG['SMA']
# print(SMG)
# Comment out Below if you need these Values in CSV Files.
SMG.plot()
# visualise the data
plt.show()
SMG.to_csv('titanMV.csv')
