from datetime import date
from django.core import validators
from django.core.mail import send_mail, EmailMessage
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.conf import settings
from localflavor.us.models import USStateField, USZipCodeField
from simple_history.models import HistoricalRecords
from simple_history.admin import SimpleHistoryAdmin


# Users will be stored in the core User model instead of a custom model.
# Default fields of the core User model: username, first_name, last_name, email, password, groups, user_permissions,
# is_staff, is_active, is_superuser, last_login, date_joined
# For more information, see: https://docs.djangoproject.com/en/1.8/ref/contrib/auth/#user


######
#
#  Abstract Base Classes
#
######


class HistoryModel(models.Model):
    """
    An abstract base class model to track creation, modification, and data change history.
    """

    created_date = models.DateField(default=date.today, null=True, blank=True, db_index=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, db_index=True,
                                   related_name='%(class)s_creator')
    modified_date = models.DateField(auto_now=True, null=True, blank=True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, db_index=True,
                                    related_name='%(class)s_modifier')
    history = HistoricalRecords()

    class Meta:
        abstract = True
        default_permissions = ('add', 'change', 'delete', 'view')


class AddressModel(HistoryModel):
    """
    An abstract base class model for common address fields.
    """

    street = models.CharField(max_length=255, blank=True)
    unit = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = USStateField(null=True, blank=True)
    zipcode = USZipCodeField(null=True, blank=True)

    class Meta:
        abstract = True


######
#
#  Determinations
#
######


class Case(HistoryModel):
    """
    An official case to document the CBRS determination for a property on behalf of a requester.
    The analyst, QC reviewer, and FWS reviewer must always be three different persons.
    """

    def _get_id(self):
        """Returns the id of the record"""
        return '%s' % self.id

    def _get_status(self):
        """Returns the status of the record"""
        if self.close_date and not self.final_letter_date:
            return 'Closed with no Final Letter'
        elif self.close_date:
            return 'Final'
        elif self.qc_reviewer_signoff_date:
            return 'Awaiting Final Letter'
        elif self.analyst_signoff_date:
            return 'Awaiting QC'
        else:
            return 'Received'

    def send_final_email(self):
        if self.final_letter_date is not None:

            cbrs_email_address = "CBRAdeterminations@fws.gov"
            other_cbrs_email_addresses = ["CBRA@fws.gov", ]

            # construct and send the final email with the final letter as attachment
            subject = "Coastal Barrier Resources Act Determination Case " + self.case_reference
            body = "Dear Requester,\r\n\r\n"
            body += "Attached is the Coastal Barrier Resources Act determination that you requested"
            body += " from the U.S. Fish and Wildlife Service. If you have any questions about this determination,"
            body += " please contact Teresa Fish, Program Specialist, at (703) 358-2171 or e-mail us at cbra@fws.gov."
            from_address = cbrs_email_address
            to_addresses_list = [self.requester.email, ]
            bcc_addresses_list = other_cbrs_email_addresses
            reply_to_list = [cbrs_email_address, ]
            headers = None  # {'Message-ID': 'foo'}
            attachments = []
            if hasattr(self, 'casefiles'):
                casefiles = CaseFile.objects.filter(case=self.id)
                for casefile in casefiles:
                    if casefile.final_letter:
                        attachments.append(casefile)
                        break
            # send_mail(subject, message, from_address, to_addresses_list, fail_silently=False)
            email = EmailMessage(subject, body, from_address, to_addresses_list, bcc_addresses_list,
                                 reply_to=reply_to_list, headers=headers, attachments=attachments)
            email.send(fail_silently=False)

    # for new records, there is a custom signal receiver in the receivers.py file listening for
    # the post_save event signal, and when the post_save's 'created' boolean is true,
    # this custom receiver will create the case hash (public ID) and send a confirmation email

    case_number = property(_get_id)
    case_reference = models.CharField(max_length=255, blank=True)
    duplicate = models.ForeignKey('self', null=True, blank=True)
    status = property(_get_status)
    request_date = models.DateField(default=date.today, null=True, blank=True)
    requester = models.ForeignKey('Requester', related_name='cases', on_delete=models.PROTECT)
    property = models.ForeignKey('Property', related_name='cases', on_delete=models.PROTECT)
    cbrs_unit = models.ForeignKey('SystemUnit', null=True, blank=True, on_delete=models.PROTECT)
    map_number = models.ForeignKey('SystemMap', null=True, blank=True, on_delete=models.PROTECT)
    cbrs_map_date = models.DateField(null=True, blank=True)
    determination = models.ForeignKey('Determination', null=True, blank=True, on_delete=models.PROTECT)
    prohibition_date = models.DateField(null=True, blank=True)
    distance = models.FloatField(null=True, blank=True)
    fws_fo_received_date = models.DateField(null=True, blank=True)
    fws_hq_received_date = models.DateField(null=True, blank=True)
    final_letter_date = models.DateField(null=True, blank=True)
    close_date = models.DateField(null=True, blank=True)
    final_letter_recipient = models.CharField(max_length=255, blank=True)
    analyst = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name='analyst', null=True, blank=True, on_delete=models.PROTECT)
    analyst_signoff_date = models.DateField(null=True, blank=True)
    qc_reviewer = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    related_name='qc_reviewer', null=True, blank=True, on_delete=models.PROTECT)
    qc_reviewer_signoff_date = models.DateField(null=True, blank=True)
    fws_reviewer = models.ForeignKey(settings.AUTH_USER_MODEL,
                                     related_name='fws_reviewer', null=True, blank=True, on_delete=models.PROTECT)
    fws_reviewer_signoff_date = models.DateField(null=True, blank=True)
    priority = models.BooleanField(default=False)
    on_hold = models.BooleanField(default=False)
    invalid = models.BooleanField(default=False)
    tags = models.ManyToManyField('Tag', through='CaseTag', related_name='cases')

    def __str__(self):
        return self.case_number

    class Meta:
        db_table = "cbrs_case"


class CaseFile(HistoryModel):
    """
    File "attached" to a case to assist with determination, which can be uploaded by either
    the requester or by CBRS staff. Can be a map, picture, letter, or any number of things.
    For easier management, file sizes will be limited to ~2MB, and file types will be limited to the following:
    txt, pdf, doc, jpeg, png, gif, tif, bmp, shp, zip, (others?).
    """

    def _get_filename(self):
        """Returns the name of the file"""
        return '%s' % str(self.file).split('/')[-1]

    def casefile_location(instance, filename):
        """Returns a custom location for the case file, in a folder named for its case"""
        # print(instance.uploader_id)
        if not instance.uploader_id:
            return 'casefiles/{0}/requester/{1}'.format(instance.case, filename)
        else:
            return 'casefiles/{0}/{1}'.format(instance.case, filename)

    name = property(_get_filename)
    file = models.FileField(upload_to=casefile_location)
    case = models.ForeignKey('Case', related_name='casefiles')
    from_requester = models.BooleanField(default=False)
    final_letter = models.BooleanField(default=False)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name="casefiles")
    uploaded_date = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = "cbrs_casefile"
        unique_together = ("file", "case")


class Property(AddressModel):
    """
    A real estate property for which a CBRS determination has been requested.
    """

    # other fields for lot number, legal descriptions, lat/lon, etc, need to be discussed
    legal_description = models.CharField(max_length=255, blank=True)
    subdivision = models.CharField(max_length=255, blank=True)
    policy_number = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.street + ", " + self.unit + ", " + self.city + ", " + self.state + ", " + self.zipcode

    class Meta:
        db_table = "cbrs_property"
        unique_together = ("street", "unit", "city", "state", "zipcode", "legal_description")
        verbose_name_plural = "properties"


class Requester(AddressModel):
    """
    Name and contact information of the person making the request for a determination.
    """

    salutation = models.CharField(max_length=16, blank=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    organization = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, blank=True, validators=[validators.EmailValidator])

    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        db_table = "cbrs_requester"
        unique_together = ("salutation", "first_name", "last_name", "organization", "email",
                           "street", "unit", "city", "state", "zipcode")


######
#
#  Tags
#
######


class CaseTag(HistoryModel):
    """
    Table to allow many-to-many relationship between Cases and Tags.
    """

    case = models.ForeignKey('Case')
    tag = models.ForeignKey('Tag')
    history = HistoricalRecords()

    def __str__(self):
        return str(self.case) + " - " + str(self.tag)

    class Meta:
        db_table = "cbrs_casetag"
        unique_together = ("case", "tag")


class Tag(HistoryModel):
    """
    Terms or keywords used to describe, categorize, or group similar Cases for easier searching and reporting.
    """

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "cbrs_tag"


######
#
#  Comments
#
######


class Comment(HistoryModel):
    """
    Comments by CBRS staff about cases. Can be used for conversations between CBRS staff about cases.
    Possibly replace this model with the Django excontrib Comments module?
    http://django-contrib-comments.readthedocs.org/en/latest/index.html
    """

    comment = models.TextField()
    acase = models.ForeignKey('Case', related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.comment

    class Meta:
        db_table = "cbrs_comment"
        unique_together = ("comment", "acase")
        ordering = ['-id']


######
#
#  Lookup Tables
#
######


class Determination(HistoryModel):
    """
    Lookup table for official determination values, which are as follows:
    "In", "Out", "Partially In; Structure In", "Partially In; Structure Out", "Partially In/No Structure".
    Property is always mentioned first, then the structure if necessary.
    """

    determination = models.CharField(max_length=32, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.determination

    class Meta:
        db_table = "cbrs_determination"


class SystemUnit(HistoryModel):
    """
    Lookup table for CBRS System Units.
    """

    system_unit_number = models.CharField(max_length=16, unique=True)
    system_unit_name = models.CharField(max_length=255, blank=True)
    system_unit_type = models.ForeignKey('SystemUnitType', on_delete=models.PROTECT)
    field_office = models.ForeignKey('FieldOffice',
                                     related_name='system_units', null=True, blank=True, on_delete=models.PROTECT)
    system_maps = models.ManyToManyField('SystemMap', through='SystemUnitMap', related_name='system_units')

    def __str__(self):
        return self.system_unit_number

    class Meta:
        db_table = "cbrs_systemunit"
        ordering = ['system_unit_number']


class SystemUnitType(HistoryModel):
    """
    Lookup table for Types for System Units.
    """

    unit_type = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return self.unit_type

    class Meta:
        db_table = "cbrs_systemunittype"
        ordering = ['unit_type']


class SystemUnitProhibitionDate(HistoryModel):
    """
    Lookup table for Prohibition Dates for System Units.
    """

    prohibition_date = models.DateField()
    system_unit = models.ForeignKey('SystemUnit', related_name='prohibition_dates', on_delete=models.CASCADE)

    def __str__(self):
        return self.prohibition_date

    class Meta:
        db_table = "cbrs_systemunitprohibitiondate"
        ordering = ['-prohibition_date']
        unique_together = ("prohibition_date", "system_unit")


class SystemUnitMap(HistoryModel):
    """
    Table to allow many-to-many relationship between System Units and Maps.
    """

    system_unit = models.ForeignKey('SystemUnit')
    system_map = models.ForeignKey('SystemMap')
    history = HistoricalRecords()

    def __str__(self):
        return str(self.system_unit) + " - " + str(self.system_map)

    class Meta:
        db_table = "cbrs_systemunitmap"
        unique_together = ("system_unit", "system_map")


class SystemMap(HistoryModel):
    """
    Lookup table for Maps for System Units.
    """

    map_number = models.CharField(max_length=16)
    map_title = models.CharField(max_length=255, blank=True)
    map_date = models.DateField()
    effective = models.BooleanField(default=True)

    def __str__(self):
        return self.map_number

    class Meta:
        db_table = "cbrs_systemmap"
        unique_together = ("map_number", "map_date")


class FieldOffice(HistoryModel):
    """
    Lookup table for Field Offices for System Units.
    """

    field_office_number = models.CharField(max_length=16, unique=True)
    field_office_name = models.CharField(max_length=255, blank=True)
    field_agent_name = models.CharField(max_length=255, blank=True)
    field_agent_email = models.CharField(max_length=255, blank=True, validators=[validators.EmailValidator])
    city = models.CharField(max_length=255, blank=True)
    state = USStateField(null=True, blank=True)

    def __str__(self):
        return self.city + ", " + self.state

    class Meta:
        db_table = "cbrs_fieldoffice"


######
#
#  Reports
#
######


class ReportCaseCountsQuerySet(models.QuerySet):
    def count_cases_by_status(self):
        count_cases = self.count_closed().copy()
        count_cases.update(self.count_closed_no_final_letter())
        count_cases.update(self.count_awaiting_final_letter())
        count_cases.update(self.count_awaiting_qc())
        count_cases.update(self.count_received())
        return count_cases

    def count_closed_no_final_letter(self):
        return self.filter(close_date__isnull=False,
                           final_letter_date__isnull=True
                           ).aggregate(count_closed_no_final_letter=models.Count('id'))

    def count_closed(self):
        return self.filter(close_date__isnull=False,
                           final_letter_date__isnull=False
                           ).aggregate(count_closed=models.Count('id'))

    def count_awaiting_final_letter(self):
        return self.filter(qc_reviewer_signoff_date__isnull=False,
                           close_date__isnull=True,
                           final_letter_date__isnull=True
                           ).aggregate(count_awaiting_final_letter=models.Count('id'))

    def count_awaiting_qc(self):
        return self.filter(analyst_signoff_date__isnull=False,
                           qc_reviewer_signoff_date__isnull=True,
                           close_date__isnull=True,
                           final_letter_date__isnull=True
                           ).aggregate(count_awaiting_level_1_qc=models.Count('id'))

    def count_received(self):
        return self.filter(analyst_signoff_date__isnull=True,
                           qc_reviewer_signoff_date__isnull=True,
                           close_date__isnull=True,
                           final_letter_date__isnull=True
                           ).aggregate(count_received=models.Count('id'))


class ReportCaseCountsManager(models.Manager):
    def get_queryset(self):
        return ReportCaseCountsQuerySet(self.model, using=self._db)

    def count_cases_by_status(self):
        return self.get_queryset().count_cases_by_status()

    def count_closed_no_final_letter(self):
        return self.get_queryset().count_closed_no_final_letter()

    def count_closed(self):
        return self.get_queryset().count_closed()

    def count_awaiting_final_letter(self):
        return self.get_queryset().count_awaiting_final_letter()

    def count_awaiting_qc(self):
        return self.get_queryset().count_awaiting_qc()

    def count_received(self):
        return self.get_queryset().count_received()


class ReportCase(Case):

    def _get_analyst_days(self):
        """Returns the number of days needed to get analyst signoff (Awaiting QC Level 1 Date - Request Date)"""
        if self.request_date and self.analyst_signoff_date:
            analyst_time = self.analyst_signoff_date - self.request_date
            return analyst_time.days
        else:
            return None

    def _get_qc_reviewer_days(self):
        """Returns the number of days needed to get qc reviewer signoff (Awaiting QC Level 2 Date - Request Date)"""
        if self.request_date and self.qc_reviewer_signoff_date:
            qc_reviewer_time = self.qc_reviewer_signoff_date - self.request_date
            return qc_reviewer_time.days
        else:
            return None

    def _get_final_letter_days(self):
        """Returns the number of days needed to get the final letter (Final Letter Date - Request Date)"""
        if self.request_date and self.final_letter_date:
            final_letter_time = self.final_letter_date - self.request_date
            return final_letter_time.days
        else:
            return None

    def _get_close_days(self):
        """Returns the number of days needed to close the case (Close Date - Request Date)"""
        if self.request_date and self.close_date:
            close_time = self.close_date - self.request_date
            return close_time.days
        else:
            return None

    analyst_days = property(_get_analyst_days)
    qc_reviewer_days = property(_get_qc_reviewer_days)
    final_letter_days = property(_get_final_letter_days)
    close_days = property(_get_close_days)
    report_case_counts = ReportCaseCountsManager()

    def __str__(self):
        return str(self.id)

    class Meta:
        proxy = True
