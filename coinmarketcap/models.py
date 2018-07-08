# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
# stands for coinmarketcap coin
class CMCCoin(models.Model):
    cmc_id = models.PositiveIntegerField()
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=10)
    website_slug = models.CharField(max_length=50)
