from delta.delta_rest_client import DeltaRestClient
from delta.delta_rest_client import OrderType
# from delta_rest_client import DeltaRestClient
from datetime import datetime
from datetime import timedelta

import time
delta_client = DeltaRestClient(
    base_url='https://testnet-api.delta.exchange',
    api_key='9ebc141cb213fbb31683f487504622',
    api_secret='3ccf098d8970f1faae5aa56bf76927eb3e579c565fb3525e22f140aeb199')


def isTimeExceed():
    order_returns = delta_client.get_orders(
        {"state": "pending", "stop_order_type": 'stop_loss_order'})
    if len(order_returns):
        order_time = order_returns[0]['created_at']
        current_time = datetime.utcnow().replace(microsecond=0)
        datetime_object = datetime.strptime(
            order_time, '%Y-%m-%dT%H:%M:%S.%f%z').strftime('%Y-%m-%d %H:%M:%S')
        time_diff = (
            current_time-datetime.strptime(datetime_object, '%Y-%m-%d %H:%M:%S'))
        print(time_diff)

        time_difference_in_minutes = time_diff / timedelta(minutes=1)
        if time_difference_in_minutes > 10:
            print('greater than 10 mins')
        else:
            print('less than 10 mins')

isTimeExceed()
    #     if
    #     order_returns = delta_client.cancel_order(16, order_returns[0]['id'])
    # order_returns = delta_client.get_orders({"state": "open"})
    # order_returns = delta_client.cancel_order(16,order_returns[0]['id'])
    # print((order_returns))
#
# print((order_returns))
# positions = delta_client.get_position(16)
# #
# pos = str(positions)
# print(pos)
# file1 = open("orders_list.txt", "w")  # append mode
# toPush = str('123123')+'\t 9990 \n'
# file1.write(toPush)
# file1.close()

# file1 = open("orders_list.txt", "r")
# data = file1.readlines()
# print(data[0])
# file1.close()

# if pos == "None":
#     print('prace oder')
#     # order_response = delta_client.place_order(
#     #     product_id=16, size=10, side='sell', limit_price='10000')
#     order_response = delta_client.place_order(
#         product_id=16, size=10, side='sell', order_type=OrderType.MARKET, take_profit_price='9932.5', trail_amount='9958.0')
#     print('', order_response)
# else:
#     print('already in push')

# # history = delta_client.order_history()
# # print('history orders', history)
# print(delta_client.get_product(16))
# order_response = delta_client.place_stop_order(
#     product_id=16, size=10, side='buy', order_type=OrderType.MARKET, stop_price='9970')

# order_response = delta_client.place_order(
#     product_id=16, size=10, side='sell', order_type=OrderType.LIMIT, limit_price='9974', client_order_id='123')
# print(order_response)
