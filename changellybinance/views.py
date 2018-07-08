# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

from changellybinance.models import PriceDelta, SMSNotificationSetting, SMSSent
from collections import defaultdict
import datetime, requests

# twilio setup
from twilio.rest import Client
account_sid = "ACcd92974e089f6b7c04805e7716d08511"
auth_token  = "46b1f6e3812de30312c03f1efbaab3d9"
client = Client(account_sid, auth_token)

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
    all_sms_settings = SMSNotificationSetting.objects.all()
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
                    for sms_setting in all_sms_settings:
                        if float_delta >= sms_setting.delta_threshold and not past_max_daily_sms_for_coin(sms_setting.phone_number, symbol):
                            send_twilio_sms(sms_setting.phone_number, symbol, delta)

                    json_response.append({new_price_delta.symbol: {'time': str(new_price_delta.time), 'delta': new_price_delta.delta}})
    return JsonResponse(json_response, safe=False)

def send_twilio_sms(phone_number, symbol, delta):
    message_body = "Arb delta found: {}, {}%".format(symbol, delta)
    message = client.messages.create(
        to=phone_number,
        from_="+19256607941",
        body=message_body)

    if (message.sid):
        SMSSent.objects.create(to=phone_number, symbol=symbol)


def past_max_daily_sms_for_coin(phone_number, symbol):
    one_day_ago = datetime.datetime.now() - datetime.timedelta(hours=24)
    num_sms_sent_in_last_24_hrs_for_coin = SMSSent.objects.filter(
        to__phone_number=phone_number,
        sent__gte=one_day_ago,
        symbol=symbol
    ).count()

    if num_sms_sent_in_last_24_hrs_for_coin > 5: # TODO this '5' should be set dynamically
        return True
    return False
