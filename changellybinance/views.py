# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from changellybinance.models import PriceDelta, CMCCoin, CoinMention, BizThread, BizThreadReply
from collections import defaultdict
import datetime, requests

# Create your views here.
def home(request):
    # data must be formatted as [{label: symbol, data: {x: time, y: delta}}, ...]
    return render(request, 'arb_graph.html')

def shill_meter(request):
    return render(request, 'shill_meter.html')

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

def scan_4chan_posts(request):
    r = requests.get('https://a.4cdn.org/biz/catalog.json')
    threads_added = []
    biz_data = r.json()
    # ignore existing threads
    existing_thread_numbers = BizThread.objects.values_list('number', flat=True)

    for page_dict in biz_data:
        threads_on_page = page_dict['threads']
        for thread in threads_on_page:
            thread_num = thread['no']
            if int(thread_num) not in existing_thread_numbers:
                try:
                    subtitle = thread['sub']
                except KeyError:
                    subtitle = None

                try:
                    comment = thread['com']
                except KeyError:
                    comment = None
                # db has never seen this thread before
                BizThread.objects.create(
                    time_int=thread['time'],
                    number=thread_num,
                    filename=thread['filename'],
                    comment=comment,
                    subtitle=subtitle,
                )

                threads_added.append(thread)
    return JsonResponse({'threads_added': threads_added}, safe=False)


def get_price_deltas(request):
    all_price_deltas = PriceDelta.objects.all()
    all_times = [time.strftime('%Y-%m-%d %H:%M') for time in PriceDelta.objects.values_list('time', flat=True).order_by('-time')]
    unique_times = []
    for time in all_times:
        if time not in unique_times:
            unique_times.append(time)

    unique_times = sorted(unique_times)


    # require all the deltas to be formatted as such
    # {times: [10-2-2018, 10-3-2018...], vib: [0.1, -0.1, 0.2, 3], 'zrs': [0.1 ...]...
    data = {'times': unique_times}
    time_to_delta = defaultdict(dict)
    for delta in all_price_deltas:
        delta_time = delta.time.strftime('%Y-%m-%d %H:%M')
        time_to_delta[delta.symbol][delta_time] = delta.delta

    for symbol in time_to_delta.keys():
        data[symbol] = []
        time_to_delta_for_symbol = time_to_delta[symbol]
        for time in unique_times:
            try:
                data[symbol].append(time_to_delta_for_symbol[time])
            except KeyError:
                # sometimes we don't always have delta at the time we're trying to plot
                # so just use 0 as a placeholder
                data[symbol].append('null')

    return JsonResponse(data, safe=False)

@csrf_exempt
def submit_price_deltas(request):
    json_response = []
    # creates a batch of new PriceDelta objects
    now = datetime.datetime.now()
    if request.POST:
        for symbol in request.POST.keys():
            delta = request.POST[symbol]
            if symbol and delta:
                # show values greater than +1% and less than -4% only
                float_delta = float(delta)
                if float_delta > 1 or float_delta < -10:
                    new_price_delta = PriceDelta.objects.create(symbol=symbol, delta=float(delta), time=now)
                    json_response.append({new_price_delta.symbol: {'time': str(new_price_delta.time), 'delta': new_price_delta.delta}})
    return JsonResponse(json_response, safe=False)
