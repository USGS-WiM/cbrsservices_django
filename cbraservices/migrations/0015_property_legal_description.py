# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cbraservices', '0014_auto_20161031_2156'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='legal_description',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
