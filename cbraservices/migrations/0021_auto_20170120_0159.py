# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cbraservices', '0020_reportcase'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='case',
            new_name='caseid',
        ),
        migrations.AlterUniqueTogether(
            name='comment',
            unique_together=set([('comment', 'caseid')]),
        ),
    ]
