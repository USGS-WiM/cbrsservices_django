# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('cbraservices', '0018_auto_20170114_1929'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportCase',
            fields=[
                ('case_id', models.IntegerField(serialize=False, primary_key=True)),
                ('case_reference', models.CharField(max_length=255)),
                ('request_date', models.DateField(default=datetime.date.today)),
                ('analyst_signoff_date', models.DateField()),
                ('qc_reviewer_signoff_date', models.DateField()),
                ('fws_reviewer_signoff_date', models.DateField()),
                ('final_letter_date', models.DateField()),
                ('close_date', models.DateField()),
            ],
            options={
                'db_table': 'cbra_case',
                'managed': False,
            },
        ),
    ]
