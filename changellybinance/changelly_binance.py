import requests
import hashlib
import hmac
import json
from collections import defaultdict

import requests

API_URL = 'https://api.changelly.com'
API_KEY = 'd3fd7f899f3f47e1918185ec2bd14e31'
API_SECRET = '0b34d5d1c9cf87388d5c7b7857683632986e672c97a0c49cc94ec42cecbd275f'

def send_query_to_changelly(message):
    serialized_data = json.dumps(message)
    sign = hmac.new(API_SECRET.encode('utf-8'), serialized_data.encode('utf-8'), hashlib.sha512).hexdigest()
    headers = {'api-key': API_KEY, 'sign': sign, 'Content-type': 'application/json'}
    response = requests.post(API_URL, headers=headers, data=serialized_data)

    return response.json()['result']
def get_binance_btc_pairs_and_prices():
    # returns a list of coins that are shared between both binance and changelly
    binance_pairs_prices_map = {}
    binance_coins = requests.get('https://api.binance.com/api/v3/ticker/price')
    for coin in binance_coins.json():
        ticker_symbol = coin['symbol']
        if 'BTC' in ticker_symbol:
            binance_pairs_prices_map[ticker_symbol] = coin['price']
    return binance_pairs_prices_map

def get_all_changelly_coins():
    message = {
      "jsonrpc": "2.0",
      "method": "getCurrenciesFull",
      "params": {},
      "id": 1
    }

    results = send_query_to_changelly(message)
    return results
# print get_all_changelly_coins()
def get_intersection_of_coins_on_changelly_and_binance(binance_pairs_prices_map):
    pairs_on_both_exchanges = []

    all_changelly_coins = get_all_changelly_coins()
    changelly_symbols = []
    for coin in all_changelly_coins:
        if coin['enabled'] == True:
            changelly_symbols.append(coin['name'].upper())

    binance_symbols = [pair.replace('BTC', '') for pair in binance_pairs_prices_map.keys()]
    for symbol in binance_symbols:
        if symbol in changelly_symbols:
            pairs_on_both_exchanges.append(symbol)

    return pairs_on_both_exchanges
# print get_intersection_of_coins_on_changelly_and_binance(get_binance_btc_pairs_and_prices())

COINS_ON_BOTH_EXCHANGES = ['OMG', 'ADX', 'ZRX', 'MCO', 'BRD', 'LSK', 'STORJ', 'XEM', 'LTC', 'BAT', 'LUN', 'NAV', 'SNM', 'STRAT', 'WAVES', 'QTUM', 'XMR', 'RLC', 'REP', 'DNT', 'PIVX', 'XRP', 'ETH', 'EOS', 'ZEN', 'USDT', 'VEN', 'RCN', 'GNT', 'TRX', 'ZEC', 'KMD', 'BNT', 'VIB', 'ETC', 'SALT']

# binance_coins_and_prices = get_binance_btc_pairs_and_prices()

def get_changelly_coins_and_prices():
    params = []
    ret = {}
    for coin in COINS_ON_BOTH_EXCHANGES:
        params.append({
            "from": "btc",
            "to": coin,
            "amount": "1"
        })

    message = {
      "jsonrpc": "2.0",
      "method": "getExchangeAmount",
      "params": params,
      "id": 1
    }

    results = send_query_to_changelly(message)
    changelly_prices = {}

    for result in results:
        price = 1 / float(result['result'])
        changelly_prices[result['to']] = price

    return changelly_prices


def get_combined_changelly_and_binance_prices():
    binance_coins_standardized = {}
    binance_coins_and_prices = get_binance_btc_pairs_and_prices()
    combined_prices = {}

    for coin in binance_coins_and_prices.keys():
        binance_coins_standardized[coin.replace('BTC', '').lower()] = binance_coins_and_prices[coin]

    changelly_coins_and_prices = get_changelly_coins_and_prices()


    for coin in changelly_coins_and_prices.keys():
        if coin not in ['qtum-i', 'usdt']:
            combined_prices[coin.lower()] = (float(binance_coins_standardized[coin]), changelly_coins_and_prices[coin])

    return combined_prices


def get_price_deltas():
    combined_prices = get_combined_changelly_and_binance_prices()
    ret = {}
    ret2 = []

    for symbol in combined_prices.keys():
        binance_price = combined_prices[symbol][0]
        changelly_price = combined_prices[symbol][1]

        delta = binance_price - changelly_price
        delta_percentage = delta / binance_price * 100

        ret[symbol] = "{0:.1f}".format(delta_percentage)
        ret2.append([str(round(delta_percentage, 2)) + "%", symbol])

    return sorted(ret2)


print get_price_deltas()
