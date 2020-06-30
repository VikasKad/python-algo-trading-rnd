import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style
import datetime as dt
import pandas as pd
import pandas_datareader.data as web

style.use('ggplot')
# start = dt.datetime(2019,9,1)
# end = dt.datetime(2019,9,15)
# df = web.DataReader('TITAN.NS','yahoo',start,end)
# df.to_csv('titan.csv')
df =pd.read_csv('titan.csv',parse_dates=True,index_col=0)
print(df[['Open','Low']].head())
df['Adj Close'].plot()
plt.show()