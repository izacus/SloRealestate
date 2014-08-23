# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('estate_ads', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdPicture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('picture_url', models.URLField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='estatead',
            name='picture',
        ),
        migrations.AddField(
            model_name='estatead',
            name='administrative_unit',
            field=models.CharField(default=None, max_length=255, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='estatead',
            name='description',
            field=models.TextField(default=None, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='estatead',
            name='pictures',
            field=models.ForeignKey(related_name=b'ad', to='estate_ads.AdPicture', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='estatead',
            name='raw_detail_html',
            field=models.TextField(default=None, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='estatead',
            name='thumbnail',
            field=models.OneToOneField(related_name=b'thumb_ad', null=True, to='estate_ads.AdPicture'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='estatead',
            name='author_name',
            field=models.CharField(default=None, max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='estatead',
            name='floor',
            field=models.CharField(default=None, max_length=8, blank=True),
        ),
        migrations.AlterField(
            model_name='estatead',
            name='short_description',
            field=models.TextField(default=None, blank=True),
        ),
    ]
