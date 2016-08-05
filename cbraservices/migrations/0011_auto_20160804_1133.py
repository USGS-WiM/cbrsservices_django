# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cbraservices', '0010_auto_20160715_1454'),
    ]

    operations = [
        migrations.CreateModel(
            name='SystemUnitType',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('created_date', models.DateField(default=datetime.datetime.now, blank=True, db_index=True, null=True)),
                ('modified_date', models.DateField(auto_now=True, null=True)),
                ('unit_type', models.CharField(unique=True, max_length=16)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, related_name='systemunittype_creator', null=True)),
                ('modified_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, related_name='systemunittype_modifier', null=True)),
            ],
            options={
                'ordering': ['unit_type'],
                'db_table': 'cbra_systemunittype',
            },
        ),
        migrations.AlterField(
            model_name='case',
            name='request_date',
            field=models.DateField(default=datetime.date(2016, 8, 4)),
        ),
    ]
