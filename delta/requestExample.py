from delta.delta_rest_client import DeltaRestClient
delta_client = DeltaRestClient(
    base_url='https://testnet-api.delta.exchange',
    api_key='9ebc141cb213fbb31683f487504622',
    api_secret='3ccf098d8970f1faae5aa56bf76927eb3e579c565fb3525e22f140aeb199')

bracket_payload = {
    "product_id": 27,                # BTCUSD
    "stop_loss_order": {
        "order_type": "market_order",
        "stop_price": "9900"
    },
    "take_profit_order": {
        "order_type": "market_order",
        "stop_price": "12991"
    }
}

response = delta_client.request(
    "POST", "orders/bracket", bracket_payload, auth=True)
response = response.json()
