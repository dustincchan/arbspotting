# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class PriceDelta(models.Model):
    symbol = models.CharField(max_length=30)
    delta = models.FloatField()
    time = models.DateTimeField(auto_now_add=True)

    def as_dict(self):
        return {self.symbol: {'delta': self.delta, 'time': str(self.time)}}

class SMSNotificationSetting(models.Model):
    phone_number = models.CharField(max_length=30, primary_key=True)
    delta_threshold = models.FloatField(default=0.0, blank=True)

class SMSSent(models.Model):
    to = models.ForeignKey(SMSNotificationSetting)
    sent = models.DateTimeField(auto_now_add=True)
