# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cbraservices', '0013_auto_20160804_1404'),
    ]

    operations = [
        migrations.AddField(
            model_name='casefile',
            name='final_letter',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='casefile',
            name='from_requester',
            field=models.BooleanField(default=False),
        ),
    ]
