# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('cbraservices', '0012_systemunit_system_unit_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='created_date',
            field=models.DateField(blank=True, default=datetime.date.today, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='case',
            name='request_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='casefile',
            name='created_date',
            field=models.DateField(blank=True, default=datetime.date.today, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='casetag',
            name='created_date',
            field=models.DateField(blank=True, default=datetime.date.today, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='created_date',
            field=models.DateField(blank=True, default=datetime.date.today, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='determination',
            name='created_date',
            field=models.DateField(blank=True, default=datetime.date.today, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='fieldoffice',
            name='created_date',
            field=models.DateField(blank=True, default=datetime.date.today, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='historicalcasetag',
            name='created_date',
            field=models.DateField(blank=True, default=datetime.date.today, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='historicalsystemunitmap',
            name='created_date',
            field=models.DateField(blank=True, default=datetime.date.today, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='created_date',
            field=models.DateField(blank=True, default=datetime.date.today, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='requester',
            name='created_date',
            field=models.DateField(blank=True, default=datetime.date.today, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='systemmap',
            name='created_date',
            field=models.DateField(blank=True, default=datetime.date.today, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='systemunit',
            name='created_date',
            field=models.DateField(blank=True, default=datetime.date.today, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='systemunitmap',
            name='created_date',
            field=models.DateField(blank=True, default=datetime.date.today, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='systemunitprohibitiondate',
            name='created_date',
            field=models.DateField(blank=True, default=datetime.date.today, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='systemunittype',
            name='created_date',
            field=models.DateField(blank=True, default=datetime.date.today, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='tag',
            name='created_date',
            field=models.DateField(blank=True, default=datetime.date.today, db_index=True, null=True),
        ),
    ]
