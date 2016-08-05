# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cbraservices', '0011_auto_20160804_1133'),
    ]

    operations = [
        migrations.AddField(
            model_name='systemunit',
            name='system_unit_type',
            field=models.ForeignKey(to='cbraservices.SystemUnitType', default=1),
            preserve_default=False,
        ),
    ]
