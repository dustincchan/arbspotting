# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-01 21:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('coinmarketcap', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BizCoinMention',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='BizThread',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('time_int', models.PositiveIntegerField()),
                ('number', models.PositiveIntegerField()),
                ('filename', models.CharField(max_length=50)),
                ('comment', models.TextField(blank=True, default=None, null=True)),
                ('subtitle', models.TextField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BizThreadReply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_int', models.PositiveIntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('number', models.PositiveIntegerField()),
                ('comment', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='bizcoinmention',
            name='biz_thread',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fourchan_scanner.BizThread'),
        ),
        migrations.AddField(
            model_name='bizcoinmention',
            name='coin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coinmarketcap.CMCCoin'),
        ),
    ]