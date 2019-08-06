# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import cbrsservices.models
import django.core.validators
from django.conf import settings
import localflavor.us.models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created_date', models.DateField(blank=True, null=True, db_index=True, default=datetime.date.today)),
                ('modified_date', models.DateField(null=True, auto_now=True)),
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
                ('priority', models.BooleanField(default=False)),
                ('on_hold', models.BooleanField(default=False)),
                ('invalid', models.BooleanField(default=False)),
                ('analyst', models.ForeignKey(blank=True, null=True, related_name='analyst', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'cbrs_case',
            },
        ),
        migrations.CreateModel(
            name='CaseFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created_date', models.DateField(blank=True, null=True, db_index=True, default=datetime.date.today)),
                ('modified_date', models.DateField(null=True, auto_now=True)),
                ('file', models.FileField(upload_to=cbrsservices.models.CaseFile.casefile_location)),
                ('from_requester', models.BooleanField(default=False)),
                ('final_letter', models.BooleanField(default=False)),
                ('uploaded_date', models.DateField(null=True, auto_now_add=True)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='case_files', to='cbrsservices.Case')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, null=True, related_name='casefile_creator', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, null=True, related_name='casefile_modifier', to=settings.AUTH_USER_MODEL)),
                ('uploader', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, null=True, related_name='case_files', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'cbrs_casefile',
            },
        ),
        migrations.CreateModel(
            name='CaseTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created_date', models.DateField(blank=True, null=True, db_index=True, default=datetime.date.today)),
                ('modified_date', models.DateField(null=True, auto_now=True)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cbrsservices.Case')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, null=True, related_name='casetag_creator', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, null=True, related_name='casetag_modifier', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'cbrs_casetag',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created_date', models.DateField(blank=True, null=True, db_index=True, default=datetime.date.today)),
                ('modified_date', models.DateField(null=True, auto_now=True)),
                ('comment', models.TextField()),
                ('acase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='cbrsservices.Case')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, null=True, related_name='comment_creator', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, null=True, related_name='comment_modifier', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'cbrs_comment',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Determination',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created_date', models.DateField(blank=True, null=True, db_index=True, default=datetime.date.today)),
                ('modified_date', models.DateField(null=True, auto_now=True)),
                ('determination', models.CharField(max_length=32, unique=True)),
                ('description', models.TextField(blank=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, null=True, related_name='determination_creator', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, null=True, related_name='determination_modifier', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'cbrs_determination',
            },
        ),
        migrations.CreateModel(
            name='FieldOffice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created_date', models.DateField(blank=True, null=True, db_index=True, default=datetime.date.today)),
                ('modified_date', models.DateField(null=True, auto_now=True)),
                ('field_office_number', models.CharField(max_length=16, unique=True)),
                ('field_office_name', models.CharField(max_length=255, blank=True)),
                ('field_agent_name', models.CharField(max_length=255, blank=True)),
                ('field_agent_email', models.CharField(max_length=255, blank=True, validators=[django.core.validators.EmailValidator])),
                ('city', models.CharField(max_length=255, blank=True)),
                ('state', localflavor.us.models.USStateField(max_length=2, blank=True, null=True, choices=[('AL', 'Alabama'), ('AK', 'Alaska'), ('AS', 'American Samoa'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('AA', 'Armed Forces Americas'), ('AE', 'Armed Forces Europe'), ('AP', 'Armed Forces Pacific'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('GU', 'Guam'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('MP', 'Northern Mariana Islands'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('PR', 'Puerto Rico'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VI', 'Virgin Islands'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')])),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, null=True, related_name='fieldoffice_creator', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, null=True, related_name='fieldoffice_modifier', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'cbrs_fieldoffice',
            },
        ),
        migrations.CreateModel(
            name='HistoricalCaseTag',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', blank=True, db_index=True, auto_created=True)),
                ('created_date', models.DateField(blank=True, null=True, db_index=True, default=datetime.date.today)),
                ('modified_date', models.DateField(blank=True, null=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('case', models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to='cbrsservices.Case', db_constraint=False)),
                ('created_by', models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, db_constraint=False)),
                ('history_user', models.ForeignKey(null=True, related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, db_constraint=False)),
            ],
            options={
                'verbose_name': 'historical case tag',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalSystemUnitMap',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', blank=True, db_index=True, auto_created=True)),
                ('created_date', models.DateField(blank=True, null=True, db_index=True, default=datetime.date.today)),
                ('modified_date', models.DateField(blank=True, null=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('created_by', models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, db_constraint=False)),
                ('history_user', models.ForeignKey(null=True, related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, db_constraint=False)),
            ],
            options={
                'verbose_name': 'historical system unit map',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created_date', models.DateField(blank=True, null=True, db_index=True, default=datetime.date.today)),
                ('modified_date', models.DateField(null=True, auto_now=True)),
                ('street', models.CharField(max_length=255, blank=True)),
                ('unit', models.CharField(max_length=255, blank=True)),
                ('city', models.CharField(max_length=255, blank=True)),
                ('state', localflavor.us.models.USStateField(max_length=2, blank=True, null=True, choices=[('AL', 'Alabama'), ('AK', 'Alaska'), ('AS', 'American Samoa'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('AA', 'Armed Forces Americas'), ('AE', 'Armed Forces Europe'), ('AP', 'Armed Forces Pacific'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('GU', 'Guam'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('MP', 'Northern Mariana Islands'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('PR', 'Puerto Rico'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VI', 'Virgin Islands'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')])),
                ('zipcode', localflavor.us.models.USZipCodeField(max_length=10, blank=True, null=True)),
                ('legal_description', models.CharField(max_length=255, blank=True)),
                ('subdivision', models.CharField(max_length=255, blank=True)),
                ('policy_number', models.CharField(max_length=255, blank=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, null=True, related_name='property_creator', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, null=True, related_name='property_modifier', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'properties',
                'db_table': 'cbrs_property',
            },
        ),
        migrations.CreateModel(
            name='Requester',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created_date', models.DateField(blank=True, null=True, db_index=True, default=datetime.date.today)),
                ('modified_date', models.DateField(null=True, auto_now=True)),
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
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, null=True, related_name='requester_creator', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, null=True, related_name='requester_modifier', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'cbrs_requester',
            },
        ),
        migrations.CreateModel(
            name='SystemMap',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created_date', models.DateField(blank=True, null=True, db_index=True, default=datetime.date.today)),
                ('modified_date', models.DateField(null=True, auto_now=True)),
                ('map_number', models.CharField(max_length=16)),
                ('map_title', models.CharField(max_length=255, blank=True)),
                ('map_date', models.DateField()),
                ('effective', models.BooleanField(default=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, null=True, related_name='systemmap_creator', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, null=True, related_name='systemmap_modifier', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'cbrs_systemmap',
            },
        ),
        migrations.CreateModel(
            name='SystemUnit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created_date', models.DateField(blank=True, null=True, db_index=True, default=datetime.date.today)),
                ('modified_date', models.DateField(null=True, auto_now=True)),
                ('system_unit_number', models.CharField(max_length=16, unique=True)),
                ('system_unit_name', models.CharField(max_length=255, blank=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, null=True, related_name='systemunit_creator', to=settings.AUTH_USER_MODEL)),
                ('field_office', models.ForeignKey(blank=True, null=True, related_name='system_units', on_delete=django.db.models.deletion.PROTECT, to='cbrsservices.FieldOffice')),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, null=True, related_name='systemunit_modifier', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'cbrs_systemunit',
                'ordering': ['system_unit_number'],
            },
        ),
        migrations.CreateModel(
            name='SystemUnitMap',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created_date', models.DateField(blank=True, null=True, db_index=True, default=datetime.date.today)),
                ('modified_date', models.DateField(null=True, auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, null=True, related_name='systemunitmap_creator', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, null=True, related_name='systemunitmap_modifier', to=settings.AUTH_USER_MODEL)),
                ('system_map', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cbrsservices.SystemMap')),
                ('system_unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cbrsservices.SystemUnit')),
            ],
            options={
                'db_table': 'cbrs_systemunitmap',
            },
        ),
        migrations.CreateModel(
            name='SystemUnitProhibitionDate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created_date', models.DateField(blank=True, null=True, db_index=True, default=datetime.date.today)),
                ('modified_date', models.DateField(null=True, auto_now=True)),
                ('prohibition_date', models.DateField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, null=True, related_name='systemunitprohibitiondate_creator', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, null=True, related_name='systemunitprohibitiondate_modifier', to=settings.AUTH_USER_MODEL)),
                ('system_unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prohibition_dates', to='cbrsservices.SystemUnit')),
            ],
            options={
                'db_table': 'cbrs_systemunitprohibitiondate',
                'ordering': ['-prohibition_date'],
            },
        ),
        migrations.CreateModel(
            name='SystemUnitType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created_date', models.DateField(blank=True, null=True, db_index=True, default=datetime.date.today)),
                ('modified_date', models.DateField(null=True, auto_now=True)),
                ('unit_type', models.CharField(max_length=16, unique=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, null=True, related_name='systemunittype_creator', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, null=True, related_name='systemunittype_modifier', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'cbrs_systemunittype',
                'ordering': ['unit_type'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created_date', models.DateField(blank=True, null=True, db_index=True, default=datetime.date.today)),
                ('modified_date', models.DateField(null=True, auto_now=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, null=True, related_name='tag_creator', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, null=True, related_name='tag_modifier', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'cbrs_tag',
            },
        ),
        migrations.AddField(
            model_name='systemunit',
            name='system_maps',
            field=models.ManyToManyField(related_name='system_units', to='cbrsservices.SystemMap', through='cbrsservices.SystemUnitMap'),
        ),
        migrations.AddField(
            model_name='systemunit',
            name='system_unit_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cbrsservices.SystemUnitType'),
        ),
        migrations.AddField(
            model_name='historicalsystemunitmap',
            name='system_map',
            field=models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to='cbrsservices.SystemMap', db_constraint=False),
        ),
        migrations.AddField(
            model_name='historicalsystemunitmap',
            name='system_unit',
            field=models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to='cbrsservices.SystemUnit', db_constraint=False),
        ),
        migrations.AddField(
            model_name='historicalcasetag',
            name='tag',
            field=models.ForeignKey(blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to='cbrsservices.Tag', db_constraint=False),
        ),
        migrations.AddField(
            model_name='casetag',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cbrsservices.Tag'),
        ),
        migrations.AddField(
            model_name='case',
            name='cbrs_unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='cbrsservices.SystemUnit'),
        ),
        migrations.AddField(
            model_name='case',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, null=True, related_name='case_creator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='case',
            name='determination',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='cbrsservices.Determination'),
        ),
        migrations.AddField(
            model_name='case',
            name='duplicate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, null=True, to='cbrsservices.Case'),
        ),
        migrations.AddField(
            model_name='case',
            name='fws_reviewer',
            field=models.ForeignKey(blank=True, null=True, related_name='fws_reviewer', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='case',
            name='map_number',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='cbrsservices.SystemMap'),
        ),
        migrations.AddField(
            model_name='case',
            name='modified_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, null=True, related_name='case_modifier', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='case',
            name='property',
            field=models.ForeignKey(related_name='cases', on_delete=django.db.models.deletion.PROTECT, to='cbrsservices.Property'),
        ),
        migrations.AddField(
            model_name='case',
            name='qc_reviewer',
            field=models.ForeignKey(blank=True, null=True, related_name='qc_reviewer', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='case',
            name='requester',
            field=models.ForeignKey(related_name='cases', on_delete=django.db.models.deletion.PROTECT, to='cbrsservices.Requester'),
        ),
        migrations.AddField(
            model_name='case',
            name='tags',
            field=models.ManyToManyField(related_name='cases', to='cbrsservices.Tag', through='cbrsservices.CaseTag'),
        ),
        migrations.CreateModel(
            name='ReportCase',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('cbrsservices.case',),
        ),
        migrations.AlterUniqueTogether(
            name='systemunitprohibitiondate',
            unique_together=set([('prohibition_date', 'system_unit')]),
        ),
        migrations.AlterUniqueTogether(
            name='systemunitmap',
            unique_together=set([('system_unit', 'system_map')]),
        ),
        migrations.AlterUniqueTogether(
            name='systemmap',
            unique_together=set([('map_number', 'map_date')]),
        ),
        migrations.AlterUniqueTogether(
            name='requester',
            unique_together=set([('salutation', 'first_name', 'last_name', 'organization', 'email', 'street', 'unit', 'city', 'state', 'zipcode')]),
        ),
        migrations.AlterUniqueTogether(
            name='property',
            unique_together=set([('street', 'unit', 'city', 'state', 'zipcode', 'legal_description')]),
        ),
        migrations.AlterUniqueTogether(
            name='comment',
            unique_together=set([('comment', 'acase')]),
        ),
        migrations.AlterUniqueTogether(
            name='casetag',
            unique_together=set([('case', 'tag')]),
        ),
        migrations.AlterUniqueTogether(
            name='casefile',
            unique_together=set([('file', 'case')]),
        ),
    ]
