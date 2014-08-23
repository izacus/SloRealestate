# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    replaces = [(b'estate_ads', '0001_initial'), (b'estate_ads', '0002_auto_20140823_1404'), (b'estate_ads', '0003_auto_20140823_1428'), (b'estate_ads', '0004_auto_20140823_1456'), (b'estate_ads', '0005_estatead_county')]

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EstateAd',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ad_id', models.CharField(unique=True, max_length=255, db_index=True)),
                ('region', models.IntegerField(db_index=True, choices=[(1, b'LJ_OKOLICA'), (2, b'J_PRIMORSKA'), (3, b'GORENJSKA'), (4, b'S_PRIMORSKA'), (5, b'SAVINJSKA'), (6, b'DOLENJSKA'), (8, b'NOTRANJSKA'), (9, b'PODRAVSKA'), (10, b'KOROSKA'), (11, b'ZASAVSKA'), (12, b'POSAVSKA'), (14, b'LJ_MESTO'), (15, b'POMURSKA')])),
                ('type', models.IntegerField(db_index=True, null=True, choices=[(0, b'PRODAJA'), (1, b'NAKUP'), (2, b'ODDAJA'), (3, b'NAJEM')])),
                ('building_type', models.IntegerField(db_index=True, null=True, choices=[(0, b'STANOVANJE'), (1, b'HISA'), (2, b'POSEST'), (3, b'POSLOVNI_PROSTOR'), (4, b'GARAZA'), (5, b'VIKEND')])),
                ('title', models.CharField(max_length=255)),
                ('link', models.URLField(max_length=255)),
                ('short_description', models.TextField(default=b'', blank=True)),
                ('author_name', models.CharField(default=b'', max_length=255, blank=True)),
                ('publish_date', models.DateTimeField()),
                ('size_m2', models.FloatField(null=True)),
                ('price_m2', models.FloatField(null=True)),
                ('price', models.FloatField(null=True)),
                ('year_built', models.IntegerField(null=True)),
                ('floor', models.CharField(default=b'', max_length=8, blank=True)),
                ('raw_data', models.TextField()),
                ('raw_html', models.TextField()),
                ('administrative_unit', models.CharField(default=b'', max_length=255, blank=True)),
                ('description', models.TextField(default=b'', blank=True)),
                ('raw_detail_html', models.TextField(default=b'', blank=True)),
                ('county', models.CharField(default=b'', max_length=255, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AdPicture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('picture_url', models.URLField(max_length=255)),
                ('ad', models.ForeignKey(to='estate_ads.EstateAd', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
