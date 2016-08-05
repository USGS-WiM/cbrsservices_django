# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('cbraservices', '0007_auto_20160325_1807'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='case_hash',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='case',
            name='request_date',
            field=models.DateField(default=datetime.date(2016, 4, 5)),
        ),
    ]
