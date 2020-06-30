from delta.delta_rest_client import DeltaRestClient
from delta.delta_rest_client import OrderType
import time
import pandas as pd
from datetime import datetime
import schedule
import requests
import urllib
import csv

symbol = 'BTCUSD'
timeInterval = 5


def callDelta(delta_client, side, limit_price, take_profit_price, trail_amount, opposite_site):
    try:
        positions = delta_client.get_position(16)
        pos = str(positions)
        if pos == "None":
            print('placing order')
            order_response = delta_client.place_stop_order(
                product_id=16, size=10, side=side, order_type=OrderType.MARKET, stop_price=limit_price)
            print('position order: \t', order_response['id'])
            row = [order_response['id'], trail_amount, opposite_site]
            with open('orders.csv', 'w') as f:
                writer = csv.writer(f)
                writer.writerow(row)
            f.close()

            order_response = delta_client.place_order(
                product_id=16, size=10, side=opposite_site, order_type=OrderType.LIMIT, limit_price=take_profit_price)
            print('take profit order:\t', order_response['id'])

        else:
            print('already in push')
    except (requests.exceptions.HTTPError, urllib.error.HTTPError) as e:
        error_msg = e.response.text
        print("Error while placing order: %s" % (error_msg))
        # cancel all orders


def initAlgorithm(processData, timestamp_arr, delta_client):
    print('------------------------Algorithm started------------------------')
    print('machine utc:\t', datetime.utcnow())
    print('timestamp(UTC):\t', datetime.utcfromtimestamp(
        int(timestamp_arr[0])).strftime('%Y-%m-%d %H:%M:%S'))
    print(processData)

    # step 2: check H(T1)>H(T2-T6)

    t1High = processData['h'].values[0]
    print('High(T1):\t', t1High)
    t1HighFlag = True
    largestHigh = 0
    i = 0
    for currentElement in processData['h']:
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

    t1Low = processData['l'].values[0]
    print('Low(T1):\t', t1Low)

    t1LowFlag = True
    # now traverse all remaining and find largest one.
    smallestLow = processData['l'].values[1]
    i = 0
    for currentElement in processData['l']:
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
    t1Close = processData['c'].values[0]
    t1Open = processData['o'].values[0]

    if t1HighFlag:
        if t1Close <= t1Open:
            print('***************placed Cover Order LIMIT SELL order***************')
            sellOrder = t1Low-2

            print('sell order at:\t', sellOrder)
            print('Take profit at:\t', sellOrder - 10)
            print('stop loss at:\t', t1High + 2)

            callDelta(delta_client, 'sell', sellOrder,
                      sellOrder - 10, t1High + 2, 'buy')
    if t1LowFlag:
        if t1Close >= t1Open:
            print('***************placed  CO LIMIT  BUY order***************')
            sellOrder = t1High+2
            print('buy order at:\t', sellOrder)
            print('Take profit at:\t', sellOrder + 10)
            print('stop loss at:\t', t1Low - 2)

            callDelta(delta_client, 'buy', sellOrder,
                      sellOrder + 10, t1Low - 2, 'sell')
    # --------------End of program so restart it again--------------


def startProgram():
    try:
        delta_client = DeltaRestClient(
            base_url='https://testnet-api.delta.exchange',
            api_key='x',
            api_secret='x')
        ohlcData = delta_client.get_price_history(symbol, 50, timeInterval)
        df = pd.DataFrame(ohlcData)
        ohlcv_data = df[['t', 'o', 'h', 'l', 'c', 'v']]
        # print(ohlcv_data)
        processData = ohlcv_data[::-1].head(6)
        timestamp_arr = processData['t'].values
        # print('machine utc:\t', datetime.utcnow())
        if timeInterval == 5:
            machine_time_minute = datetime.utcnow().strftime("%M")
            if machine_time_minute[1] == '0' or machine_time_minute[1] == '5':
                initAlgorithm(processData, timestamp_arr, delta_client)
            else:
                print('we are not checking algorithm')

        else:
            print('started for 1 min')
            initAlgorithm(processData, timestamp_arr, delta_client)

    except (requests.exceptions.HTTPError, urllib.error.HTTPError) as e:
        error_msg = e.response.text
        print("Error while placing order: %s" % (error_msg))


startProgram()


# schedule.every(1).minutes.at(':01').do(startProgram)
# while True:
#     schedule.run_pending()
