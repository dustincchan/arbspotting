import requests

def sync_with_coinmarketcap():
    symbols = {}
    coin_names = {}
    # names are more unique than 'symbol', so we should use that to find new coins
    existing_coin_names_set = set(CMCCoin.objects.values_list('name', flat=True))

    cmc_coin_request = requests.get('https://api.coinmarketcap.com/v2/listings/')
    data = cmc_coin_request.json()['data']
    for coin in data:
        if coin['name'] in existing_coin_names_set:




r = requests.get('https://a.4cdn.org/biz/catalog.json')
biz_data = r.json()
