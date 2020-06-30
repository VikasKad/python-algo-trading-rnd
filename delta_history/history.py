from delta.delta_rest_client import DeltaRestClient
from delta.delta_rest_client import OrderType
import time
import pandas as pd
from datetime import datetime, timedelta
import requests
import urllib
symbol = 'BTCUSD'
timeInterval = 5


def startProgram():
    try:
        delta_client = DeltaRestClient(
            base_url='https://testnet-api.delta.exchange',
            api_key='9ebc141cb213fbb31683f487504622',
            api_secret='3ccf098d8970f1faae5aa56bf76927eb3e579c565fb3525e22f140aeb199')
        start_time = datetime.now() - timedelta(days=3)
        end_time = datetime.now() - timedelta(days=2)

        start_time = int(start_time.strftime("%s"))
        end_time = int(end_time.strftime("%s"))
        # print(start_time, end_time)
        ohlcData = delta_client.get_price_history_by_time(
            symbol, start_time, end_time,  resolution=5)
        df = pd.DataFrame(ohlcData)
        # ohlcv_data = df[['t', 'o', 'h', 'l', 'c', 'v']]
        totalLength = len(df['t'])
        print('total', totalLength)
        # print(df.between_time(ohlcData['t'][0],ohlcData['t'][5]))
        # for i in range(5, 10):
        #     df["new_index"] = range(5, 10)
        #     df = df.set_index("new_index")

        # init_time =datetime.fromtimestamp((ohlcData['t'][i]))
        # end_time =datetime.fromtimestamp((ohlcData['t'][i+6]))
        # print('initial_time', init_time)

    except (requests.exceptions.HTTPError, urllib.error.HTTPError) as e:
        error_msg = e.response.text
        print("Error while placing order: %s" % (error_msg))


startProgram()
