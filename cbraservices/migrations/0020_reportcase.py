# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cbraservices', '0019_reportcase'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportCase',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('cbraservices.case',),
        ),
    ]
