# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import localflavor.us.models
import django.core.validators
import datetime
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created_date', models.DateField(db_index=True, default=datetime.datetime.now, blank=True, null=True)),
                ('modified_date', models.DateField(auto_now=True, null=True)),
                ('request_date', models.DateField(default=datetime.datetime.now)),
                ('cbrs_map_date', models.DateField(blank=True, null=True)),
                ('prohibition_date', models.DateField(blank=True, null=True)),
                ('distance', models.FloatField(null=True)),
                ('fws_fo_received_date', models.DateField(blank=True, null=True)),
                ('fws_hq_received_date', models.DateField(blank=True, null=True)),
                ('final_letter_date', models.DateField(blank=True, null=True)),
                ('close_date', models.DateField(blank=True, null=True)),
                ('final_letter_recipient', models.CharField(max_length=255, blank=True)),
                ('analyst_signoff_date', models.DateField(blank=True, null=True)),
                ('qc_reviewer_signoff_date', models.DateField(blank=True, null=True)),
                ('fws_reviewer_signoff_date', models.DateField(blank=True, null=True)),
                ('priority', models.BooleanField(default=False)),
                ('analyst', models.ForeignKey(null=True, blank=True, to=settings.AUTH_USER_MODEL, related_name='analyst')),
            ],
            options={
                'db_table': 'cbra_case',
            },
        ),
        migrations.CreateModel(
            name='CaseFile',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created_date', models.DateField(db_index=True, default=datetime.datetime.now, blank=True, null=True)),
                ('modified_date', models.DateField(auto_now=True, null=True)),
                ('file', models.FileField(blank=True, upload_to='cbraservices.DatabaseFile/bytes/filename/mimetype', null=True)),
                ('uploaded_date', models.DateField(auto_now_add=True, null=True)),
                ('case', models.ForeignKey(to='cbraservices.Case', related_name='case_files')),
            ],
            options={
                'db_table': 'cbra_casefile',
            },
        ),
        migrations.CreateModel(
            name='CaseTag',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created_date', models.DateField(db_index=True, default=datetime.datetime.now, blank=True, null=True)),
                ('modified_date', models.DateField(auto_now=True, null=True)),
                ('case', models.ForeignKey(to='cbraservices.Case')),
            ],
            options={
                'db_table': 'cbra_casetag',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created_date', models.DateField(db_index=True, default=datetime.datetime.now, blank=True, null=True)),
                ('modified_date', models.DateField(auto_now=True, null=True)),
                ('comment', models.TextField()),
                ('case', models.ForeignKey(to='cbraservices.Case', related_name='comments')),
            ],
            options={
                'db_table': 'cbra_comment',
            },
        ),
        migrations.CreateModel(
            name='DatabaseFile',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('bytes', models.TextField()),
                ('filename', models.CharField(max_length=255)),
                ('mimetype', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'cbra_databasefile',
            },
        ),
        migrations.CreateModel(
            name='Determination',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created_date', models.DateField(db_index=True, default=datetime.datetime.now, blank=True, null=True)),
                ('modified_date', models.DateField(auto_now=True, null=True)),
                ('determination', models.CharField(max_length=32, unique=True)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'db_table': 'cbra_determination',
            },
        ),
        migrations.CreateModel(
            name='FieldOffice',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created_date', models.DateField(db_index=True, default=datetime.datetime.now, blank=True, null=True)),
                ('modified_date', models.DateField(auto_now=True, null=True)),
                ('field_office_number', models.CharField(max_length=16, unique=True)),
                ('field_office_name', models.CharField(max_length=255, blank=True)),
                ('field_agent_name', models.CharField(max_length=255, blank=True)),
                ('field_agent_email', models.CharField(validators=[django.core.validators.EmailValidator], max_length=255, blank=True)),
                ('city', models.CharField(max_length=255, blank=True)),
                ('state', localflavor.us.models.USStateField(blank=True, choices=[('AL', 'Alabama'), ('AK', 'Alaska'), ('AS', 'American Samoa'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('AA', 'Armed Forces Americas'), ('AE', 'Armed Forces Europe'), ('AP', 'Armed Forces Pacific'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('GU', 'Guam'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('MP', 'Northern Mariana Islands'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('PR', 'Puerto Rico'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VI', 'Virgin Islands'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')], max_length=2, null=True)),
            ],
            options={
                'db_table': 'cbra_fieldoffice',
            },
        ),
        migrations.CreateModel(
            name='HistoricalCaseTag',
            fields=[
                ('id', models.IntegerField(auto_created=True, db_index=True, verbose_name='ID', blank=True)),
                ('created_date', models.DateField(db_index=True, default=datetime.datetime.now, blank=True, null=True)),
                ('modified_date', models.DateField(blank=True, editable=False, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('case', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, blank=True, to='cbraservices.Case', db_constraint=False, related_name='+')),
                ('history_user', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, null=True, to=settings.AUTH_USER_MODEL, related_name='+')),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical case tag',
            },
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created_date', models.DateField(db_index=True, default=datetime.datetime.now, blank=True, null=True)),
                ('modified_date', models.DateField(auto_now=True, null=True)),
                ('street', models.CharField(max_length=255, blank=True)),
                ('unit', models.CharField(max_length=255, blank=True)),
                ('city', models.CharField(max_length=255, blank=True)),
                ('state', localflavor.us.models.USStateField(blank=True, choices=[('AL', 'Alabama'), ('AK', 'Alaska'), ('AS', 'American Samoa'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('AA', 'Armed Forces Americas'), ('AE', 'Armed Forces Europe'), ('AP', 'Armed Forces Pacific'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('GU', 'Guam'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('MP', 'Northern Mariana Islands'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('PR', 'Puerto Rico'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VI', 'Virgin Islands'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')], max_length=2, null=True)),
                ('zipcode', localflavor.us.models.USZipCodeField(blank=True, max_length=10, null=True)),
                ('subdivision', models.CharField(max_length=255, blank=True)),
                ('policy_number', models.CharField(max_length=255, blank=True)),
            ],
            options={
                'verbose_name_plural': 'properties',
                'db_table': 'cbra_property',
            },
        ),
        migrations.CreateModel(
            name='Requester',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created_date', models.DateField(db_index=True, default=datetime.datetime.now, blank=True, null=True)),
                ('modified_date', models.DateField(auto_now=True, null=True)),
                ('street', models.CharField(max_length=255, blank=True)),
                ('unit', models.CharField(max_length=255, blank=True)),
                ('city', models.CharField(max_length=255, blank=True)),
                ('state', localflavor.us.models.USStateField(blank=True, choices=[('AL', 'Alabama'), ('AK', 'Alaska'), ('AS', 'American Samoa'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('AA', 'Armed Forces Americas'), ('AE', 'Armed Forces Europe'), ('AP', 'Armed Forces Pacific'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('GU', 'Guam'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('MP', 'Northern Mariana Islands'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('PR', 'Puerto Rico'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VI', 'Virgin Islands'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')], max_length=2, null=True)),
                ('zipcode', localflavor.us.models.USZipCodeField(blank=True, max_length=10, null=True)),
                ('salutation', models.CharField(max_length=16, blank=True)),
                ('first_name', models.CharField(max_length=255, blank=True)),
                ('last_name', models.CharField(max_length=255, blank=True)),
                ('organization', models.CharField(max_length=255, blank=True)),
                ('email', models.CharField(validators=[django.core.validators.EmailValidator], max_length=255, blank=True)),
            ],
            options={
                'db_table': 'cbra_requester',
            },
        ),
        migrations.CreateModel(
            name='SystemMap',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created_date', models.DateField(db_index=True, default=datetime.datetime.now, blank=True, null=True)),
                ('modified_date', models.DateField(auto_now=True, null=True)),
                ('map_number', models.CharField(max_length=16, unique=True)),
                ('map_title', models.CharField(max_length=255, blank=True)),
                ('map_date', models.DateField()),
            ],
            options={
                'db_table': 'cbra_systemmap',
            },
        ),
        migrations.CreateModel(
            name='SystemUnit',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created_date', models.DateField(db_index=True, default=datetime.datetime.now, blank=True, null=True)),
                ('modified_date', models.DateField(auto_now=True, null=True)),
                ('system_unit_number', models.CharField(max_length=16, unique=True)),
                ('system_unit_name', models.CharField(max_length=255, blank=True)),
                ('field_office', models.ForeignKey(null=True, blank=True, to='cbraservices.FieldOffice', related_name='system_units')),
            ],
            options={
                'db_table': 'cbra_systemunit',
            },
        ),
        migrations.CreateModel(
            name='SystemUnitProhibitionDate',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created_date', models.DateField(db_index=True, default=datetime.datetime.now, blank=True, null=True)),
                ('modified_date', models.DateField(auto_now=True, null=True)),
                ('prohibition_date', models.DateField()),
                ('system_unit', models.ForeignKey(to='cbraservices.SystemUnit', related_name='prohibition_dates')),
            ],
            options={
                'db_table': 'cbra_systemunitprohibitiondate',
                'ordering': ['-prohibition_date'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created_date', models.DateField(db_index=True, default=datetime.datetime.now, blank=True, null=True)),
                ('modified_date', models.DateField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'db_table': 'cbra_tag',
            },
        ),
        migrations.AddField(
            model_name='systemmap',
            name='system_unit',
            field=models.ForeignKey(to='cbraservices.SystemUnit', related_name='system_maps'),
        ),
        migrations.AlterUniqueTogether(
            name='requester',
            unique_together=set([('salutation', 'first_name', 'last_name', 'organization', 'email', 'street', 'unit', 'city', 'state', 'zipcode')]),
        ),
        migrations.AlterUniqueTogether(
            name='property',
            unique_together=set([('street', 'unit', 'city', 'state', 'zipcode')]),
        ),
        migrations.AddField(
            model_name='historicalcasetag',
            name='tag',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, blank=True, to='cbraservices.Tag', db_constraint=False, related_name='+'),
        ),
        migrations.AddField(
            model_name='casetag',
            name='tag',
            field=models.ForeignKey(to='cbraservices.Tag'),
        ),
        migrations.AddField(
            model_name='case',
            name='cbrs_unit',
            field=models.ForeignKey(null=True, blank=True, to='cbraservices.SystemUnit'),
        ),
        migrations.AddField(
            model_name='case',
            name='determination',
            field=models.ForeignKey(null=True, blank=True, to='cbraservices.Determination'),
        ),
        migrations.AddField(
            model_name='case',
            name='fws_reviewer',
            field=models.ForeignKey(null=True, blank=True, to=settings.AUTH_USER_MODEL, related_name='fws_reviewer'),
        ),
        migrations.AddField(
            model_name='case',
            name='map_number',
            field=models.ForeignKey(null=True, blank=True, to='cbraservices.SystemMap'),
        ),
        migrations.AddField(
            model_name='case',
            name='property',
            field=models.ForeignKey(to='cbraservices.Property'),
        ),
        migrations.AddField(
            model_name='case',
            name='qc_reviewer',
            field=models.ForeignKey(null=True, blank=True, to=settings.AUTH_USER_MODEL, related_name='qc_reviewer'),
        ),
        migrations.AddField(
            model_name='case',
            name='requester',
            field=models.ForeignKey(to='cbraservices.Requester'),
        ),
        migrations.AddField(
            model_name='case',
            name='tags',
            field=models.ManyToManyField(to='cbraservices.Tag', through='cbraservices.CaseTag', related_name='cases'),
        ),
        migrations.AlterUniqueTogether(
            name='systemunitprohibitiondate',
            unique_together=set([('prohibition_date', 'system_unit')]),
        ),
        migrations.AlterUniqueTogether(
            name='systemmap',
            unique_together=set([('map_number', 'system_unit')]),
        ),
        migrations.AlterUniqueTogether(
            name='comment',
            unique_together=set([('comment', 'case')]),
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
