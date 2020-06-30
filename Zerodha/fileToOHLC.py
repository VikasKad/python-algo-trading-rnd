import pandas as pd
# from threading import Timer
import pymongo
import schedule
import time

"""
    step 4: If A1 is true,
    check if close is equal or lower than open.
    If yes, place Cover Order limit order at price 1 unit less than low of T1.
    Take profile: 4 units & SL is 2 units above high of t1
"""


def databaseConnect():
    print('database connection')


def sellOrder(sellPrice):
    print('sell order:\t', sellPrice)
    print('take profile\t', sellPrice+3)


def buyOrder(buyPrice):
    print('Buy Order:\t', buyPrice)


def startAlgorithm():
    df = pd.read_csv('/Users/cex/Documents/vikas/RnD/AlgoTrading/backend/CRUDEOILM19OCTFUT.csv', names=[
        'last_price', 'time'], index_col=1, parse_dates=True)

    dfTime = pd.read_csv('/Users/cex/Documents/vikas/RnD/AlgoTrading/backend/CRUDEOILM19OCTFUT.csv', names=[
        'time', 'data'], index_col=0, parse_dates=True)

    df = pd.DataFrame(df)
    df = df.tail(5000)
    # print(df)
    traverseData = df['last_price'].resample('1min').ohlc()
    # reverse the data so we can select last 6 data

    # step 1: get last 6 mins data-> t1 should be latest
    processData = traverseData[::-1].head(6)
    # print(processData)
    time_arr = dfTime[::-1].values
    print('------------------------Algorithm started------------------------')
    print('timestamp\t', time_arr[0][0])
    print(processData)
    processArray = processData.values

    # step 2: check H(T1)>H(T2-T6)
    t1High = processArray[0][1]
    print('High(T1):\t', t1High)
    t1HighFlag = True
    largestHigh = 0
    i = 0
    for currentElement in processArray:
        if i > 0:
            if currentElement[1] > largestHigh:
                largestHigh = currentElement[1]
        i += 1
    print('High(T2-T6):\t', largestHigh)
    if t1High > largestHigh:
        t1HighFlag = True
    else:
        t1HighFlag = False
    print('A1 Flag:\t', t1HighFlag)

    # step 3: check L(T1)>L(T2-T6)

    t1Low = processArray[0][2]
    print('Low(T1):\t', t1Low)

    t1LowFlag = True
    # now traverse all remaining and find largest one.
    smallestLow = processArray[1][2]
    i = 0
    for currentElement in processArray:
        if i > 0:
            if currentElement[2] < smallestLow:
                smallestLow = currentElement[2]
        i += 1

    print('Low(T2-T6):\t', smallestLow)
    if t1Low < smallestLow:
        t1LowFlag = True
    else:
        t1LowFlag = False
    print('A2 Flag:\t', t1LowFlag)
    """
        step 4: If A1 is true,
        check if close is equal or lower than open.
        If yes, place Cover Order limit order at price 1 unit less than low of T1.
        Take profile: 4 units & SL is 2 units above high of t1
    """

    t1Close = processArray[0][3]
    t1Open = processArray[0][0]
    if t1HighFlag:
        if t1Close <= t1Open:
            print('***************place Cover Order LIMIT SELL order***************')
            sellOrder = t1Low-1

            print('sell order at:\t', sellOrder)
            print('Take profit at:\t', sellOrder - 4)
            print('stop loss at:\t', t1High + 2)

            # sellOrder(t1Low - 1)
    if t1LowFlag:
        if t1Close >= t1Open:
            print('***************place  CO LIMIT  BUY order***************')
            sellOrder = t1High+1
            print('buy order at:\t', sellOrder)
            print('Take profit at:\t', sellOrder + 4)
            print('stop loss at:\t', t1Low - 2)

    # --------------End of program so restart it again--------------
    # Timer(60.0, startAlgorithm).start()


# initial call
# startAlgorithm()
# databaseConnect()


schedule.every(1).minutes.at(':00').do(startAlgorithm)
while True:
    schedule.run_pending()