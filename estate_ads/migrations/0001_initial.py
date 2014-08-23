# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

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
                ('picture', models.URLField(max_length=255, null=True)),
                ('short_description', models.TextField(null=True)),
                ('author_name', models.CharField(max_length=255, null=True)),
                ('publish_date', models.DateTimeField()),
                ('size_m2', models.FloatField(null=True)),
                ('price_m2', models.FloatField(null=True)),
                ('price', models.FloatField(null=True)),
                ('year_built', models.IntegerField(null=True)),
                ('floor', models.CharField(max_length=8, null=True)),
                ('raw_data', models.TextField()),
                ('raw_html', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
