# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from coinmarketcap.models import CMCCoin

# Create your models here.
class BizThread(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    time_int = models.PositiveIntegerField()
    number = models.PositiveIntegerField()
    filename = models.CharField(max_length=50)
    comment = models.TextField(blank=True, null=True, default=None)
    subtitle = models.TextField(blank=True, null=True, default=None)

class BizCoinMention(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    coin = models.ForeignKey(CMCCoin)
    biz_thread = models.ForeignKey(BizThread)

class BizThreadReply(models.Model):
    time_int = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    number = models.PositiveIntegerField()
    comment = models.TextField()
