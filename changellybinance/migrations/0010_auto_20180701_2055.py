# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-01 20:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('changellybinance', '0009_bizcoinmention_biz_thread'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bizcoinmention',
            name='biz_thread',
        ),
        migrations.RemoveField(
            model_name='bizcoinmention',
            name='coin',
        ),
        migrations.DeleteModel(
            name='BizThreadReply',
        ),
        migrations.DeleteModel(
            name='BizCoinMention',
        ),
        migrations.DeleteModel(
            name='BizThread',
        ),
        migrations.DeleteModel(
            name='CMCCoin',
        ),
    ]