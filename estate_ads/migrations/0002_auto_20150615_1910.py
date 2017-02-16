# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('estate_ads', '0001_squashed_0005_estatead_county'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estatead',
            name='building_type',
            field=models.IntegerField(db_index=True, null=True, choices=[(0, b'Stanovanje'), (1, b'Hi\xc5\xa1a'), (2, b'Posest'), (3, b'Poslovni prostor'), (4, b'Gara\xc5\xbea'), (5, b'Vikend')]),
        ),
        migrations.AlterField(
            model_name='estatead',
            name='region',
            field=models.IntegerField(db_index=True, choices=[(1, b'Ljubljana - okolica'), (2, b'Ju\xc5\xbena primorska'), (3, b'Gorenjska'), (4, b'Severna primorska'), (5, b'Savinjska'), (6, b'Dolenjska'), (8, b'Notranjska'), (9, b'Podravska'), (10, b'Koro\xc5\xa1ka'), (11, b'Zasavska'), (12, b'Posavska'), (14, b'Ljubljana - mesto'), (15, b'Pomurska')]),
        ),
        migrations.AlterField(
            model_name='estatead',
            name='type',
            field=models.IntegerField(db_index=True, null=True, choices=[(0, b'Prodaja'), (1, b'Nakup'), (2, b'Oddaja'), (3, b'Najem')]),
        ),
    ]
