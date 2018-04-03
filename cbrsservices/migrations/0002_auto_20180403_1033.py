# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('cbrsservices', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='casefile',
            name='case',
            field=models.ForeignKey(related_name='casefiles', to='cbrsservices.Case'),
        ),
        migrations.AlterField(
            model_name='casefile',
            name='uploader',
            field=models.ForeignKey(blank=True, null=True, related_name='casefiles', to=settings.AUTH_USER_MODEL),
        ),
    ]
