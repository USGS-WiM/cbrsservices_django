# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('cbraservices', '0009_auto_20160408_0902'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-id']},
        ),
        migrations.AddField(
            model_name='case',
            name='invalid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='case',
            name='on_hold',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='case',
            name='request_date',
            field=models.DateField(default=datetime.date(2016, 7, 15)),
        ),
    ]
