# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cbraservices', '0015_property_legal_description'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='property',
            unique_together=set([('street', 'unit', 'city', 'state', 'zipcode', 'legal_description')]),
        ),
    ]
