# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

def fourchan_scanner(request):
    return render(request, 'shill_meter.html')

def update_fourchan_posts(request):
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
