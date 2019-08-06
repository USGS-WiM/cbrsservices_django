# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import datetime
import django.core.validators
from django.conf import settings
import localflavor.us.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cbrsservices', '0002_auto_20180403_1033'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalCase',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', blank=True, db_index=True, auto_created=True)),
                ('created_date', models.DateField(blank=True, null=True, db_index=True, default=datetime.date.today)),
                ('modified_date', models.DateField(blank=True, null=True, editable=False)),
                ('case_reference', models.CharField(max_length=255, blank=True)),
                ('request_date', models.DateField(blank=True, null=True, default=datetime.date.today)),
                ('cbrs_map_date', models.DateField(blank=True, null=True)),
                ('prohibition_date', models.DateField(blank=True, null=True)),
                ('distance', models.FloatField(blank=True, null=True)),
                ('fws_fo_received_date', models.DateField(blank=True, null=True)),
                ('fws_hq_received_date', models.DateField(blank=True, null=True)),
                ('final_letter_date', models.DateField(blank=True, null=True)),
                ('close_date', models.DateField(blank=True, null=True)),
                ('final_letter_recipient', models.CharField(max_length=255, blank=True)),
                ('analyst_signoff_date', models.DateField(blank=True, null=True)),
                ('qc_reviewer_signoff_date', models.DateField(blank=True, null=True)),
                ('fws_reviewer_signoff_date', models.DateField(blank=True, null=True)),
                ('hard_copy_map_reviewed', models.BooleanField(default=False)),
                ('priority', models.BooleanField(default=False)),
                ('on_hold', models.BooleanField(default=False)),
                ('invalid', models.BooleanField(default=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('analyst', models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, db_constraint=False)),
                ('cbrs_unit', models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to='cbrsservices.SystemUnit', db_constraint=False)),
                ('created_by', models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, db_constraint=False)),
                ('determination', models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to='cbrsservices.Determination', db_constraint=False)),
            ],
            options={
                'verbose_name': 'historical case',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalCaseFile',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', blank=True, db_index=True, auto_created=True)),
                ('created_date', models.DateField(blank=True, null=True, db_index=True, default=datetime.date.today)),
                ('modified_date', models.DateField(blank=True, null=True, editable=False)),
                ('file', models.TextField(max_length=100)),
                ('from_requester', models.BooleanField(default=False)),
                ('final_letter', models.BooleanField(default=False)),
                ('uploaded_date', models.DateField(blank=True, null=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
            ],
            options={
                'verbose_name': 'historical case file',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalComment',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', blank=True, db_index=True, auto_created=True)),
                ('created_date', models.DateField(blank=True, null=True, db_index=True, default=datetime.date.today)),
                ('modified_date', models.DateField(blank=True, null=True, editable=False)),
                ('comment', models.TextField()),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
            ],
            options={
                'verbose_name': 'historical comment',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalDetermination',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', blank=True, db_index=True, auto_created=True)),
                ('created_date', models.DateField(blank=True, null=True, db_index=True, default=datetime.date.today)),
                ('modified_date', models.DateField(blank=True, null=True, editable=False)),
                ('determination', models.CharField(max_length=32, db_index=True)),
                ('description', models.TextField(blank=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('created_by', models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, db_constraint=False)),
                ('history_user', models.ForeignKey(null=True, related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, db_constraint=False)),
            ],
            options={
                'verbose_name': 'historical determination',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalFieldOffice',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', blank=True, db_index=True, auto_created=True)),
                ('created_date', models.DateField(blank=True, null=True, db_index=True, default=datetime.date.today)),
                ('modified_date', models.DateField(blank=True, null=True, editable=False)),
                ('field_office_number', models.CharField(max_length=16, db_index=True)),
                ('field_office_name', models.CharField(max_length=255, blank=True)),
                ('field_agent_name', models.CharField(max_length=255, blank=True)),
                ('field_agent_email', models.CharField(max_length=255, blank=True, validators=[django.core.validators.EmailValidator])),
                ('city', models.CharField(max_length=255, blank=True)),
                ('state', localflavor.us.models.USStateField(max_length=2, blank=True, null=True, choices=[('AL', 'Alabama'), ('AK', 'Alaska'), ('AS', 'American Samoa'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('AA', 'Armed Forces Americas'), ('AE', 'Armed Forces Europe'), ('AP', 'Armed Forces Pacific'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('GU', 'Guam'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('MP', 'Northern Mariana Islands'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('PR', 'Puerto Rico'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VI', 'Virgin Islands'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')])),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('created_by', models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, db_constraint=False)),
                ('history_user', models.ForeignKey(null=True, related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, db_constraint=False)),
            ],
            options={
                'verbose_name': 'historical field office',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalProperty',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', blank=True, db_index=True, auto_created=True)),
                ('created_date', models.DateField(blank=True, null=True, db_index=True, default=datetime.date.today)),
                ('modified_date', models.DateField(blank=True, null=True, editable=False)),
                ('street', models.CharField(max_length=255, blank=True)),
                ('unit', models.CharField(max_length=255, blank=True)),
                ('city', models.CharField(max_length=255, blank=True)),
                ('state', localflavor.us.models.USStateField(max_length=2, blank=True, null=True, choices=[('AL', 'Alabama'), ('AK', 'Alaska'), ('AS', 'American Samoa'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('AA', 'Armed Forces Americas'), ('AE', 'Armed Forces Europe'), ('AP', 'Armed Forces Pacific'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('GU', 'Guam'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('MP', 'Northern Mariana Islands'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('PR', 'Puerto Rico'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VI', 'Virgin Islands'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')])),
                ('zipcode', localflavor.us.models.USZipCodeField(max_length=10, blank=True, null=True)),
                ('legal_description', models.CharField(max_length=255, blank=True)),
                ('subdivision', models.CharField(max_length=255, blank=True)),
                ('policy_number', models.CharField(max_length=255, blank=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('created_by', models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, db_constraint=False)),
                ('history_user', models.ForeignKey(null=True, related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, db_constraint=False)),
            ],
            options={
                'verbose_name': 'historical property',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalReportCase',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', blank=True, db_index=True, auto_created=True)),
                ('created_date', models.DateField(blank=True, null=True, db_index=True, default=datetime.date.today)),
                ('modified_date', models.DateField(blank=True, null=True, editable=False)),
                ('case_reference', models.CharField(max_length=255, blank=True)),
                ('request_date', models.DateField(blank=True, null=True, default=datetime.date.today)),
                ('cbrs_map_date', models.DateField(blank=True, null=True)),
                ('prohibition_date', models.DateField(blank=True, null=True)),
                ('distance', models.FloatField(blank=True, null=True)),
                ('fws_fo_received_date', models.DateField(blank=True, null=True)),
                ('fws_hq_received_date', models.DateField(blank=True, null=True)),
                ('final_letter_date', models.DateField(blank=True, null=True)),
                ('close_date', models.DateField(blank=True, null=True)),
                ('final_letter_recipient', models.CharField(max_length=255, blank=True)),
                ('analyst_signoff_date', models.DateField(blank=True, null=True)),
                ('qc_reviewer_signoff_date', models.DateField(blank=True, null=True)),
                ('fws_reviewer_signoff_date', models.DateField(blank=True, null=True)),
                ('hard_copy_map_reviewed', models.BooleanField(default=False)),
                ('priority', models.BooleanField(default=False)),
                ('on_hold', models.BooleanField(default=False)),
                ('invalid', models.BooleanField(default=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('analyst', models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, db_constraint=False)),
                ('cbrs_unit', models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to='cbrsservices.SystemUnit', db_constraint=False)),
                ('created_by', models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, db_constraint=False)),
                ('determination', models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to='cbrsservices.Determination', db_constraint=False)),
            ],
            options={
                'verbose_name': 'historical report case',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalRequester',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', blank=True, db_index=True, auto_created=True)),
                ('created_date', models.DateField(blank=True, null=True, db_index=True, default=datetime.date.today)),
                ('modified_date', models.DateField(blank=True, null=True, editable=False)),
                ('street', models.CharField(max_length=255, blank=True)),
                ('unit', models.CharField(max_length=255, blank=True)),
                ('city', models.CharField(max_length=255, blank=True)),
                ('state', localflavor.us.models.USStateField(max_length=2, blank=True, null=True, choices=[('AL', 'Alabama'), ('AK', 'Alaska'), ('AS', 'American Samoa'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('AA', 'Armed Forces Americas'), ('AE', 'Armed Forces Europe'), ('AP', 'Armed Forces Pacific'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('GU', 'Guam'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('MP', 'Northern Mariana Islands'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('PR', 'Puerto Rico'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VI', 'Virgin Islands'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')])),
                ('zipcode', localflavor.us.models.USZipCodeField(max_length=10, blank=True, null=True)),
                ('salutation', models.CharField(max_length=16, blank=True)),
                ('first_name', models.CharField(max_length=255, blank=True)),
                ('last_name', models.CharField(max_length=255, blank=True)),
                ('organization', models.CharField(max_length=255, blank=True)),
                ('email', models.CharField(max_length=255, blank=True, validators=[django.core.validators.EmailValidator])),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('created_by', models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, db_constraint=False)),
                ('history_user', models.ForeignKey(null=True, related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, db_constraint=False)),
            ],
            options={
                'verbose_name': 'historical requester',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalSystemMap',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', blank=True, db_index=True, auto_created=True)),
                ('created_date', models.DateField(blank=True, null=True, db_index=True, default=datetime.date.today)),
                ('modified_date', models.DateField(blank=True, null=True, editable=False)),
                ('map_number', models.CharField(max_length=16)),
                ('map_title', models.CharField(max_length=255, blank=True)),
                ('map_date', models.DateField()),
                ('effective', models.BooleanField(default=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('created_by', models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, db_constraint=False)),
                ('history_user', models.ForeignKey(null=True, related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, db_constraint=False)),
            ],
            options={
                'verbose_name': 'historical system map',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalSystemUnit',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', blank=True, db_index=True, auto_created=True)),
                ('created_date', models.DateField(blank=True, null=True, db_index=True, default=datetime.date.today)),
                ('modified_date', models.DateField(blank=True, null=True, editable=False)),
                ('system_unit_number', models.CharField(max_length=16, db_index=True)),
                ('system_unit_name', models.CharField(max_length=255, blank=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('created_by', models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, db_constraint=False)),
                ('field_office', models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to='cbrsservices.FieldOffice', db_constraint=False)),
                ('history_user', models.ForeignKey(null=True, related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, db_constraint=False)),
                ('system_unit_type', models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to='cbrsservices.SystemUnitType', db_constraint=False)),
            ],
            options={
                'verbose_name': 'historical system unit',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalSystemUnitProhibitionDate',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', blank=True, db_index=True, auto_created=True)),
                ('created_date', models.DateField(blank=True, null=True, db_index=True, default=datetime.date.today)),
                ('modified_date', models.DateField(blank=True, null=True, editable=False)),
                ('prohibition_date', models.DateField()),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('created_by', models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, db_constraint=False)),
                ('history_user', models.ForeignKey(null=True, related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, db_constraint=False)),
                ('system_unit', models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to='cbrsservices.SystemUnit', db_constraint=False)),
            ],
            options={
                'verbose_name': 'historical system unit prohibition date',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalSystemUnitType',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', blank=True, db_index=True, auto_created=True)),
                ('created_date', models.DateField(blank=True, null=True, db_index=True, default=datetime.date.today)),
                ('modified_date', models.DateField(blank=True, null=True, editable=False)),
                ('unit_type', models.CharField(max_length=16, db_index=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('created_by', models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, db_constraint=False)),
                ('history_user', models.ForeignKey(null=True, related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, db_constraint=False)),
            ],
            options={
                'verbose_name': 'historical system unit type',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalTag',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', blank=True, db_index=True, auto_created=True)),
                ('created_date', models.DateField(blank=True, null=True, db_index=True, default=datetime.date.today)),
                ('modified_date', models.DateField(blank=True, null=True, editable=False)),
                ('name', models.CharField(max_length=255, db_index=True)),
                ('description', models.TextField(blank=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('created_by', models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, db_constraint=False)),
                ('history_user', models.ForeignKey(null=True, related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, db_constraint=False)),
            ],
            options={
                'verbose_name': 'historical tag',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.AddField(
            model_name='case',
            name='hard_copy_map_reviewed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalreportcase',
            name='duplicate',
            field=models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to='cbrsservices.Case', db_constraint=False),
        ),
        migrations.AddField(
            model_name='historicalreportcase',
            name='fws_reviewer',
            field=models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, db_constraint=False),
        ),
        migrations.AddField(
            model_name='historicalreportcase',
            name='history_user',
            field=models.ForeignKey(null=True, related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalreportcase',
            name='map_number',
            field=models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to='cbrsservices.SystemMap', db_constraint=False),
        ),
        migrations.AddField(
            model_name='historicalreportcase',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, db_constraint=False),
        ),
        migrations.AddField(
            model_name='historicalreportcase',
            name='property',
            field=models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to='cbrsservices.Property', db_constraint=False),
        ),
        migrations.AddField(
            model_name='historicalreportcase',
            name='qc_reviewer',
            field=models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, db_constraint=False),
        ),
        migrations.AddField(
            model_name='historicalreportcase',
            name='requester',
            field=models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to='cbrsservices.Requester', db_constraint=False),
        ),
        migrations.AddField(
            model_name='historicalcomment',
            name='acase',
            field=models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to='cbrsservices.Case', db_constraint=False),
        ),
        migrations.AddField(
            model_name='historicalcomment',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, db_constraint=False),
        ),
        migrations.AddField(
            model_name='historicalcomment',
            name='history_user',
            field=models.ForeignKey(null=True, related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalcomment',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, db_constraint=False),
        ),
        migrations.AddField(
            model_name='historicalcasefile',
            name='case',
            field=models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to='cbrsservices.Case', db_constraint=False),
        ),
        migrations.AddField(
            model_name='historicalcasefile',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, db_constraint=False),
        ),
        migrations.AddField(
            model_name='historicalcasefile',
            name='history_user',
            field=models.ForeignKey(null=True, related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalcasefile',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, db_constraint=False),
        ),
        migrations.AddField(
            model_name='historicalcasefile',
            name='uploader',
            field=models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, db_constraint=False),
        ),
        migrations.AddField(
            model_name='historicalcase',
            name='duplicate',
            field=models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to='cbrsservices.Case', db_constraint=False),
        ),
        migrations.AddField(
            model_name='historicalcase',
            name='fws_reviewer',
            field=models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, db_constraint=False),
        ),
        migrations.AddField(
            model_name='historicalcase',
            name='history_user',
            field=models.ForeignKey(null=True, related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalcase',
            name='map_number',
            field=models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to='cbrsservices.SystemMap', db_constraint=False),
        ),
        migrations.AddField(
            model_name='historicalcase',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, db_constraint=False),
        ),
        migrations.AddField(
            model_name='historicalcase',
            name='property',
            field=models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to='cbrsservices.Property', db_constraint=False),
        ),
        migrations.AddField(
            model_name='historicalcase',
            name='qc_reviewer',
            field=models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, db_constraint=False),
        ),
        migrations.AddField(
            model_name='historicalcase',
            name='requester',
            field=models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to='cbrsservices.Requester', db_constraint=False),
        ),
    ]
