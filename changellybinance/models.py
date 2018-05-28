# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class PriceDelta(models.Model):
    symbol = models.CharField(max_length=30)
    delta = models.FloatField()
    time = models.DateTimeField(auto_now_add=True)

    def as_dict(self):
        return {self.symbol: {'delta': self.delta, 'time': str(self.time)}}
