# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-28 03:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('changellybinance', '0007_auto_20180625_1504'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CoinMention',
            new_name='BizCoinMention',
        ),
    ]
