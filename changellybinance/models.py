# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class PriceDelta(models.Model):
    symbol = models.CharField(max_length=30)
    delta = models.FloatField()
    time = models.DateTimeField(auto_now_add=True)

    def as_dict(self):
        return {self.symbol: {'delta': self.delta, 'time': str(self.time)}}

# stands for coinmarketcap coin
class CMCCoin(models.Model):
    cmc_id = models.PositiveIntegerField()
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=10)
    website_slug = models.CharField(max_length=50)

class CoinMention(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    coin = models.ForeignKey(CMCCoin)

class BizThread(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    time_int = models.PositiveIntegerField()
    number = models.PositiveIntegerField()
    filename = models.CharField(max_length=50)
    comment = models.TextField(blank=True, null=True, default=None)
    subtitle = models.TextField(blank=True, null=True, default=None)

class BizThreadReply(models.Model):
    time_int = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    number = models.PositiveIntegerField()
    comment = models.TextField()
