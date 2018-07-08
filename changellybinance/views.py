# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

from changellybinance.models import PriceDelta, SMSNotificationSetting
from collections import defaultdict
import datetime, requests

# Create your views here.
def home(request):
    # data must be formatted as [{label: symbol, data: {x: time, y: delta}}, ...]
    data = {'sms_users': SMSNotificationSetting.objects.all()}
    return render(request, 'arb_graph.html', context=data)

def delete_all_arb_data(request):
    PriceDelta.objects.all().delete()
    return JsonResponse({'success': True})

def scan_for_4chan_coin_mentions_from_all_threads(request):
    # for now just from thread themselves and not the responses
    pass

def add_sms_notification_number(request):
    phone_number = request.GET.get('phone_number')
    delta_threshold = request.GET.get('delta_threshold')

    try:
        delta_threshold = float(delta_threshold)
    except ValueError:
        delta_threshold = 0.0

    SMSNotificationSetting.objects.create(
        phone_number=phone_number,
        delta_threshold=delta_threshold,
    )
    return render_sms_user_table(request)

def remove_number(request):
    phone_number = request.GET.get('pk')
    sms = SMSNotificationSetting.objects.get(pk=phone_number.strip())
    sms.delete()
    return render_sms_user_table(request)

def render_sms_user_table(request):
    data = {'sms_users': SMSNotificationSetting.objects.all()}
    return render(request, 'sms_user_table.html', context=data)


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
