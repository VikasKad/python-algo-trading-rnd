import time
import requests
headers = {
    'Accept': 'application/json'
}
candles_timestamp = 1
end_timestamp = int(time.time()*1)
end_timestamp = end_timestamp*1000
start_timestamp = (end_timestamp - 100 * 60 * 1000)

r = requests.get('https://api.delta.exchange/chart/history',
                 params={"symbol": 'BTCUSD', 'from': start_timestamp, 'to': end_timestamp, 'resolution': candles_timestamp}, headers=headers)

print(r.json())
