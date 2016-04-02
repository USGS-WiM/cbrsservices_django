# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('cbraservices', '0002_auto_20160304_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='request_date',
            field=models.DateField(default=datetime.date(2016, 3, 4)),
        ),
    ]
