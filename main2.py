import sys
from decimal import Decimal as D
import requests
import time
import hashlib
import hmac

from requests.api import get


def gen_sign(method, url, query_string=None, payload_string=None):
        key = API_KEY        # api_key
        secret = SECRET_KEY     # api_secret

        t = time.time()
        m = hashlib.sha512()
        m.update((payload_string or "").encode('utf-8'))
        hashed_payload = m.hexdigest()
        s = '%s\n%s\n%s\n%s\n%s' % (method, url, query_string or "", hashed_payload, t)
        sign = hmac.new(secret.encode('utf-8'), s.encode('utf-8'), hashlib.sha512).hexdigest()
        return {'KEY': key, 'Timestamp': str(t), 'SIGN': sign}


def get_ticker(symbol):
    host = "https://api.gateio.ws"
    prefix = "/api/v4"
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    
    url = '/spot/tickers'
    query_param = '?currency_pair='+symbol
    r = requests.request('GET', host + prefix + url+query_param, headers=headers)
    return r.json()



def place_order(symbol, price, quantity, trade_type, order_type):
    host = "https://api.gateio.ws"
    prefix = "/api/v4"
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    url = '/spot/orders'    
    body='{"account":"spot","currency_pair":"' + symbol + '","type":"' + order_type + '","side":"' + trade_type + '","amount":"' + str(quantity) + '","price":"' + str(price) + '"}'
    sign_headers = gen_sign('POST', prefix + url,"", body)
    headers.update(sign_headers)
    r = requests.request('POST', host + prefix + url, headers=headers, data=body)
    return r


if __name__ == '__main__':
    global API_KEY
    global SECRET_KEY

    API_KEY = sys.argv[1]
    SECRET_KEY = sys.argv[2]
    USDT = int(sys.argv[3])
    rate = int(sys.argv[4])
    multipler = float(sys.argv[5])
    sleep = int(sys.argv[6])
    symbol = sys.argv[7]
    
    
    symbol = symbol+"_USDT"

    y = get_ticker(symbol)
    order = float(y[0]['last']) * (rate + 100) * 0.01
    count = USDT / order

    res = place_order(symbol, str(order), count, 'buy', 'limit')
    print(res.json())

    if res.status_code == 200:
        print("Placed Buy\n")
        if sleep != 0:
            time.sleep(sleep)
        print(str(order) + "----------" + str(order*multipler))
        res = place_order(symbol, str(order * multipler), str(count - (count * 0.2 / 100)), 'sell', 'limit')
        print(res.json())
        if res.status_code == 200:
            print("\nPlaced Sell\n")