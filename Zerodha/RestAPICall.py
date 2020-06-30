import logging
from kiteconnect import KiteConnect

logging.basicConfig(level=logging.DEBUG)

kite = KiteConnect(api_key="e8aavxmpwesxybqt")

# Redirect the user to the login url obtained
# from kite.login_url(), and receive the request_token
# from the registered redirect url after the login flow.
# Once you have the request_token, obtain the access_token
# as follows.
# reqToken = kite.login_url()
# print(reqToken)
data = kite.generate_session(
    'o05SEpqqKmSCeome0Hl7PV3OVnvYZMvQ', api_secret="uojmcx5wqk9406nn4ja00ili7mfpiqds")
kite.set_access_token(data["access_token"])
print(data)

instruments = kite.instruments(exchange='NSE')
# instruments.to_csv('instruments.csv')
# historyData = kite.historical_data('')
# # Place an order
# try:
#     order_id = kite.place_order(tradingsymbol="INFY",
#                                 exchange=kite.EXCHANGE_NSE,
#                                 transaction_type=kite.TRANSACTION_TYPE_BUY,
#                                 quantity=1,
#                                 order_type=kite.ORDER_TYPE_MARKET,
#                                 product=kite.PRODUCT_NRML)

#     logging.info("Order placed. ID is: {}".format(order_id))
# except Exception as e:
#     logging.info("Order placement failed: {}".format(e.message))

# # Fetch all orders
# kite.orders()

# # Get instruments
# kite.instruments()

# # Place an mutual fund order
# kite.place_mf_order(
#     tradingsymbol="INF090I01239",
#     transaction_type=kite.TRANSACTION_TYPE_BUY,
#     amount=5000,
#     tag="mytag"
# )

# # Cancel a mutual fund order
# kite.cancel_mf_order(order_id="order_id")

# # Get mutual fund instruments
# kite.mf_instruments()
