# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('estate_ads', '0002_auto_20150615_1910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estatead',
            name='floor',
            field=models.CharField(default=b'', max_length=32, blank=True),
        ),
    ]
