# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cbraservices', '0021_auto_20170120_0159'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='caseid',
            new_name='acase',
        ),
        migrations.AlterUniqueTogether(
            name='comment',
            unique_together=set([('comment', 'acase')]),
        ),
    ]
