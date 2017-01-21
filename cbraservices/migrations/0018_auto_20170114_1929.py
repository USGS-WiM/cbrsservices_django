# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('cbraservices', '0017_case_legacy_case_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='case',
            name='legacy_case_number',
        ),
        migrations.AddField(
            model_name='case',
            name='duplicate',
            field=models.ForeignKey(null=True, to='cbraservices.Case', blank=True),
        ),
        migrations.AlterField(
            model_name='case',
            name='request_date',
            field=models.DateField(blank=True, default=datetime.date.today, null=True),
        ),
    ]
