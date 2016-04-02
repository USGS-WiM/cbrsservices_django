# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.db.models.deletion
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cbraservices', '0005_auto_20160304_1558'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalSystemUnitMap',
            fields=[
                ('id', models.IntegerField(db_index=True, auto_created=True, blank=True, verbose_name='ID')),
                ('created_date', models.DateField(db_index=True, null=True, blank=True, default=datetime.datetime.now)),
                ('modified_date', models.DateField(null=True, blank=True, editable=False)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('created_by', models.ForeignKey(db_constraint=False, blank=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, related_name='+', null=True)),
                ('history_user', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, related_name='+', null=True)),
                ('modified_by', models.ForeignKey(db_constraint=False, blank=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, related_name='+', null=True)),
            ],
            options={
                'get_latest_by': 'history_date',
                'ordering': ('-history_date', '-history_id'),
                'verbose_name': 'historical system unit map',
            },
        ),
        migrations.CreateModel(
            name='SystemUnitMap',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('created_date', models.DateField(db_index=True, null=True, blank=True, default=datetime.datetime.now)),
                ('modified_date', models.DateField(null=True, auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, related_name='systemunitmap_creator', null=True)),
                ('modified_by', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, related_name='systemunitmap_modifier', null=True)),
            ],
            options={
                'db_table': 'cbra_systemunitmap',
            },
        ),
        migrations.AlterField(
            model_name='case',
            name='property',
            field=models.ForeignKey(related_name='cases', to='cbraservices.Property'),
        ),
        migrations.AlterField(
            model_name='case',
            name='request_date',
            field=models.DateField(default=datetime.date(2016, 3, 24)),
        ),
        migrations.AlterField(
            model_name='case',
            name='requester',
            field=models.ForeignKey(related_name='cases', to='cbraservices.Requester'),
        ),
        migrations.AlterUniqueTogether(
            name='systemmap',
            unique_together=set([]),
        ),
        migrations.AddField(
            model_name='systemunitmap',
            name='system_map',
            field=models.ForeignKey(to='cbraservices.SystemMap'),
        ),
        migrations.AddField(
            model_name='systemunitmap',
            name='system_unit',
            field=models.ForeignKey(to='cbraservices.SystemUnit'),
        ),
        migrations.AddField(
            model_name='historicalsystemunitmap',
            name='system_map',
            field=models.ForeignKey(db_constraint=False, blank=True, on_delete=django.db.models.deletion.DO_NOTHING, to='cbraservices.SystemMap', related_name='+', null=True),
        ),
        migrations.AddField(
            model_name='historicalsystemunitmap',
            name='system_unit',
            field=models.ForeignKey(db_constraint=False, blank=True, on_delete=django.db.models.deletion.DO_NOTHING, to='cbraservices.SystemUnit', related_name='+', null=True),
        ),
        migrations.RemoveField(
            model_name='systemmap',
            name='system_unit',
        ),
        migrations.AlterUniqueTogether(
            name='systemunitmap',
            unique_together=set([('system_unit', 'system_map')]),
        ),
    ]
