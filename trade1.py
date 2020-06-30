import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style
import datetime as dt
import pandas as pd
import pandas_datareader.data as web
import datetime

style.use('ggplot')
df =pd.read_csv('TITANF1.csv',parse_dates=True,index_col=0)
print(df)
# print(df[['Open','Low']].head())