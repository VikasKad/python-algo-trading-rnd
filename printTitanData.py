import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style
import datetime as dt
import pandas as pd
import pandas_datareader.data as web

style.use('ggplot')
start = dt.datetime(2019,9,1)
end = dt.datetime(2019,9,15)
df = web.DataReader('TITAN.NS','yahoo',start,end)
print(df.head(6))