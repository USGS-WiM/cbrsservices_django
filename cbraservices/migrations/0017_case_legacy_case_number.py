# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cbraservices', '0016_auto_20161110_2214'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='legacy_case_number',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
