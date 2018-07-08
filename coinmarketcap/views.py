# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

def sync_coin_list_with_coinmarketcap(request):
    symbols = {}
    coin_names = {}
    new_coins_added = 0
    # names are more unique than 'symbol', so we should use that to find new coins
    existing_coin_names_set = set(CMCCoin.objects.values_list('name', flat=True))

    cmc_coin_request = requests.get('https://api.coinmarketcap.com/v2/listings/')
    data = cmc_coin_request.json()['data']
    for coin in data:
        coin_name = coin['name']
        if coin_name not in existing_coin_names_set:
            # we've encountered a new coin, so let's add it to our database
            coin, created = CMCCoin.objects.get_or_create(
                cmc_id=coin['id'],
                name=coin_name,
                symbol=coin['symbol'],
                website_slug=coin['website_slug'],
            )
            new_coins_added += 1
            print ("added to database: {}".format((coin.name, coin.symbol)))


    return JsonResponse({'num_coins_added': new_coins_added})
