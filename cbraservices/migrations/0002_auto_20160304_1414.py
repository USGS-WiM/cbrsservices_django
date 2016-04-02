# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import cbraservices.models
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cbraservices', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DatabaseFile',
        ),
        migrations.AddField(
            model_name='casefile',
            name='uploader',
            field=models.ForeignKey(related_name='case_files', default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='case',
            name='distance',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='case',
            name='request_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='casefile',
            name='file',
            field=models.FileField(default='casefiles/test.png', upload_to=cbraservices.models.CaseFile.casefile_location),
            preserve_default=False,
        ),
    ]
