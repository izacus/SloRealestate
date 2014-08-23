# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('estate_ads', '0002_auto_20140823_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estatead',
            name='administrative_unit',
            field=models.CharField(default=b'', max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='estatead',
            name='author_name',
            field=models.CharField(default=b'', max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='estatead',
            name='description',
            field=models.TextField(default=b'', blank=True),
        ),
        migrations.AlterField(
            model_name='estatead',
            name='floor',
            field=models.CharField(default=b'', max_length=8, blank=True),
        ),
        migrations.AlterField(
            model_name='estatead',
            name='raw_detail_html',
            field=models.TextField(default=b'', blank=True),
        ),
        migrations.AlterField(
            model_name='estatead',
            name='short_description',
            field=models.TextField(default=b'', blank=True),
        ),
    ]
