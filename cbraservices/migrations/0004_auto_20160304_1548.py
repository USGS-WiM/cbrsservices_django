# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cbraservices', '0003_auto_20160304_1424'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='created_by',
            field=models.ForeignKey(default=1, related_name='case_creator', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='case',
            name='modified_by',
            field=models.ForeignKey(default=1, related_name='case_modifier', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='casefile',
            name='created_by',
            field=models.ForeignKey(default=1, related_name='casefile_creator', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='casefile',
            name='modified_by',
            field=models.ForeignKey(default=1, related_name='casefile_modifier', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='casetag',
            name='created_by',
            field=models.ForeignKey(default=1, related_name='casetag_creator', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='casetag',
            name='modified_by',
            field=models.ForeignKey(default=1, related_name='casetag_modifier', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comment',
            name='created_by',
            field=models.ForeignKey(default=1, related_name='comment_creator', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comment',
            name='modified_by',
            field=models.ForeignKey(default=1, related_name='comment_modifier', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='determination',
            name='created_by',
            field=models.ForeignKey(default=1, related_name='determination_creator', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='determination',
            name='modified_by',
            field=models.ForeignKey(default=1, related_name='determination_modifier', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fieldoffice',
            name='created_by',
            field=models.ForeignKey(default=1, related_name='fieldoffice_creator', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fieldoffice',
            name='modified_by',
            field=models.ForeignKey(default=1, related_name='fieldoffice_modifier', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicalcasetag',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, blank=True, related_name='+', null=True, db_constraint=False, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalcasetag',
            name='modified_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, blank=True, related_name='+', null=True, db_constraint=False, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='property',
            name='created_by',
            field=models.ForeignKey(default=1, related_name='property_creator', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='property',
            name='modified_by',
            field=models.ForeignKey(default=1, related_name='property_modifier', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='requester',
            name='created_by',
            field=models.ForeignKey(default=1, related_name='requester_creator', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='requester',
            name='modified_by',
            field=models.ForeignKey(default=1, related_name='requester_modifier', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='systemmap',
            name='created_by',
            field=models.ForeignKey(default=1, related_name='systemmap_creator', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='systemmap',
            name='modified_by',
            field=models.ForeignKey(default=1, related_name='systemmap_modifier', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='systemunit',
            name='created_by',
            field=models.ForeignKey(default=1, related_name='systemunit_creator', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='systemunit',
            name='modified_by',
            field=models.ForeignKey(default=1, related_name='systemunit_modifier', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='systemunitprohibitiondate',
            name='created_by',
            field=models.ForeignKey(default=1, related_name='systemunitprohibitiondate_creator', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='systemunitprohibitiondate',
            name='modified_by',
            field=models.ForeignKey(default=1, related_name='systemunitprohibitiondate_modifier', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tag',
            name='created_by',
            field=models.ForeignKey(default=1, related_name='tag_creator', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tag',
            name='modified_by',
            field=models.ForeignKey(default=1, related_name='tag_modifier', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
