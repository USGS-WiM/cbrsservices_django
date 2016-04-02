# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('cbraservices', '0006_auto_20160324_1733'),
    ]

    operations = [
        migrations.AddField(
            model_name='systemunit',
            name='system_maps',
            field=models.ManyToManyField(related_name='system_units', to='cbraservices.SystemMap', through='cbraservices.SystemUnitMap'),
        ),
        migrations.AlterField(
            model_name='case',
            name='request_date',
            field=models.DateField(default=datetime.date(2016, 3, 25)),
        ),
        migrations.AlterField(
            model_name='systemmap',
            name='map_number',
            field=models.CharField(max_length=16),
        ),
        migrations.AlterUniqueTogether(
            name='systemmap',
            unique_together=set([('map_number', 'map_date')]),
        ),
    ]
