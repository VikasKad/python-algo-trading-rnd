import requests
import time
import pandas as pd
from datetime import datetime
import schedule
from deribit_api import RestClient

client = RestClient("KXMzYANK", "pwGwsMp5Ftp9g1C7-qMUj1KR6ME8R_fkYuHRhDEdQwE", 'https://testapp.deribit.com')
client.index()
client.account()


def startAlgorithm():
    base_url = "https://testapp.deribit.com/api/v2/public/get_tradingview_chart_data?"
    candles_timestamp = 1
    end_timestamp = int(time.time()*1)
    end_timestamp = end_timestamp*1000
    start_timestamp = (end_timestamp - 100 * 60 * 1000)
    instrument_name = 'BTC-PERPETUAL'
    resolution = candles_timestamp
    finalUrl = str('end_timestamp='+str(end_timestamp) +
                   '&instrument_name='+instrument_name+'&resolution='+str(resolution)+'&start_timestamp='+str(start_timestamp))
    r = requests.get(url=base_url+finalUrl)
    data = r.json()
    ticks = data['result']['ticks']
    df = pd.DataFrame(data['result'])
    ohlcv_data = df[['ticks', 'open', 'high', 'low', 'close', 'volume']]
    processData = ohlcv_data[::-1].head(6)
    print('------------------------Algorithm started------------------------')
    timestamp_arr = processData['ticks'].values
    print('timestamp(UTC):\t', datetime.utcfromtimestamp(
        int(timestamp_arr[0])/1000).strftime('%Y-%m-%d %H:%M:%S'))
    print(processData)

    # step 2: check H(T1)>H(T2-T6)

    t1High = processData['high'].values[0]
    print('High(T1):\t', t1High)
    t1HighFlag = True
    largestHigh = 0
    i = 0
    for currentElement in processData['high']:
        if i > 0:
            if currentElement > largestHigh:
                largestHigh = currentElement
        i += 1
    print('High(T2-T6):\t', largestHigh)
    if t1High > largestHigh:
        t1HighFlag = True
    else:
        t1HighFlag = False
    print('A1 Flag:\t', t1HighFlag)

    # step 3: check L(T1)>L(T2-T6)

    t1Low = processData['low'].values[0]
    print('Low(T1):\t', t1Low)

    t1LowFlag = True
    # now traverse all remaining and find largest one.
    smallestLow = processData['low'].values[1]
    i = 0
    for currentElement in processData['low']:
        if i > 0:
            if currentElement < smallestLow:
                smallestLow = currentElement
        i += 1
    print('Low(T2-T6):\t', smallestLow)
    if t1Low < smallestLow:
        t1LowFlag = True
    else:
        t1LowFlag = False
    print('A2 Flag:\t', t1LowFlag)
    t1Close = processData['close'].values[0]
    t1Open = processData['open'].values[0]
    """
        step 4: If A1 is true,
        check if close is equal or lower than open.
        If yes, place Cover Order limit order at price 1 unit less than low of T1.
        Take profile: 4 units & SL is 2 units above high of t1
    """
    if t1HighFlag:
        if t1Close <= t1Open:
            print('***************place Cover Order LIMIT SELL order***************')
            sellOrder = t1Low-1

            print('sell order at:\t', sellOrder)
            print('Take profit at:\t', sellOrder - 4)
            print('stop loss at:\t', t1High + 2)
            client.sell(instrument_name, 0.1, sellOrder, '1M')
    if t1LowFlag:
        if t1Close >= t1Open:
            print('***************place  CO LIMIT  BUY order***************')
            sellOrder = t1High+1
            print('buy order at:\t', sellOrder)
            print('Take profit at:\t', sellOrder + 4)
            print('stop loss at:\t', t1Low - 2)
            client.buy(instrument_name, 0.1, sellOrder, '1M')

    # --------------End of program so restart it again--------------


# startAlgorithm()
schedule.every(1).minutes.at(':59').do(startAlgorithm)
while True:
    schedule.run_pending()
