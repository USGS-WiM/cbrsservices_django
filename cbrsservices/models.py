from datetime import date
from django.core import validators
from django.core.mail import EmailMessage
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from localflavor.us.models import USStateField, USZipCodeField
from simple_history.models import HistoricalRecords


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

    created_date = models.DateField(default=date.today, null=True, blank=True, db_index=True, help_text='The date the object was created in "YYYY-MM-DD" format')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,null=True, blank=True,
                                    db_index=True, related_name='%(class)s_creator', help_text='The user who created the object')
    modified_date = models.DateField(auto_now=True, null=True, blank=True, help_text='The date the object was last modified in "YYYY-MM-DD" format')
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True,
                                    db_index=True, related_name='%(class)s_modifier', help_text='The user who last modified the object')
    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True
        default_permissions = ('add', 'change', 'delete', 'view')


class AddressModel(HistoryModel):
    """
    An abstract base class model for common address fields.
    """

    street = models.CharField(max_length=255, blank=True, help_text='The street name of the address')
    unit = models.CharField(max_length=255, blank=True, help_text='The unit at which the address is located')
    city = models.CharField(max_length=255, blank=True, help_text='The city in which the address is located')
    state = USStateField(null=True, blank=True, help_text='The state in which the address is located')
    zipcode = USZipCodeField(null=True, blank=True, help_text='The zipcode at which the address is located')

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
                                 reply_to=reply_to_list, headers=headers)
            email.attach_file(attachments[0].file.path)
            email.send(fail_silently=False)

    # for new records, there is a custom signal receiver in the receivers.py file listening for
    # the post_save event signal, and when the post_save's 'created' boolean is true,
    # this custom receiver will create the case hash (public ID) and send a confirmation email

    case_number = property(_get_id)
    case_reference = models.CharField(max_length=255, blank=True, help_text="The alphanumeric case reference")
    duplicate = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, help_text="If the case is a duplicate, indicates the ID of the original case")
    status = property(_get_status)
    request_date = models.DateField(default=date.today, null=True, blank=True, help_text='Date the case request was submitted in "YYYY-MM-DD" format')
    requester = models.ForeignKey('Requester', on_delete=models.PROTECT, related_name='cases', help_text="A foreign key integer value identifying the person who submitted the case request")
    property = models.ForeignKey('Property', on_delete=models.PROTECT, related_name='cases', help_text="A foreign key integer value identifying the property")
    cbrs_unit = models.ForeignKey('SystemUnit', on_delete=models.PROTECT, null=True, blank=True, help_text="A foreign key integer value identifying the cbrs unit closest to/containing the property")
    map_number = models.ForeignKey('SystemMap', on_delete=models.PROTECT, null=True, blank=True, help_text="A foreign key integer value identifying a system map containing the property")
    cbrs_map_date = models.DateField(null=True, blank=True, help_text='The system map date in "YYYY-MM-DD" format')
    determination = models.ForeignKey('Determination', on_delete=models.PROTECT, null=True, blank=True, help_text="A foreign key integer value identifying the determination of the property")
    prohibition_date = models.DateField(null=True, blank=True, help_text='The flood insurance prohibition date in "YYYY-MM-DD" format')
    distance = models.FloatField(null=True, blank=True, help_text="A number representing the distance the property is from a system unit")
    fws_fo_received_date = models.DateField(null=True, blank=True, help_text='The field office received date in "YYYY-MM-DD" format')
    fws_hq_received_date = models.DateField(null=True, blank=True, help_text='The headquarters received date in "YYYY-MM-DD" format')
    final_letter_date = models.DateField(null=True, blank=True, help_text='The final letter date in "YYYY-MM-DD" format')
    close_date = models.DateField(null=True, blank=True, help_text='The date the case was closed in "YYYY-MM-DD" format')
    final_letter_recipient = models.CharField(max_length=255, blank=True, help_text="The full name of the final letter recepient")
    analyst = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                related_name='analyst', null=True, blank=True, help_text="A foreign key integer value identifying the user who analyzed the case")
    analyst_signoff_date = models.DateField(null=True, blank=True, help_text='The date the analyst signed off in "YYYY-MM-DD" format')
    qc_reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                    related_name='qc_reviewer', null=True, blank=True, help_text="A foreign key integer value identifying the QC reviewer")
    qc_reviewer_signoff_date = models.DateField(null=True, blank=True, help_text='The date the QC reviewer signed off in "YYYY-MM-DD" format')
    fws_reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                     related_name='fws_reviewer', null=True, blank=True, help_text="A foreign key integer value identifying the FWS reviewer")
    fws_reviewer_signoff_date = models.DateField(null=True, blank=True, help_text='The date the FWS reviewer signed off in "YYYY-MM-DD" format')
    priority = models.BooleanField(default=False, help_text="A boolean value indicating if the case is a priority")
    on_hold = models.BooleanField(default=False, help_text="A boolean value indicating if the case is on hold")
    invalid = models.BooleanField(default=False, help_text="A boolean value indicating if the case is invalid")
    hard_copy_map_reviewed = models.BooleanField(default=False, help_text="A boolean value indicating if the hard copy of the system map has been reviewed")
    tags = models.ManyToManyField('Tag', through='CaseTag', related_name='cases', help_text="A many to many relationship of tags based on a foreign key integer value identifying a tag")
    # TODO: add requester fields here???

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

    def casefile_location(self, instance, filename):
        """Returns a custom location for the case file, in a folder named for its case"""
        if not instance.uploader_id:
            return 'casefiles/{0}/requester/{1}'.format(instance.case, filename)
        else:
            return 'casefiles/{0}/{1}'.format(instance.case, filename)

    name = property(_get_filename)
    file = models.FileField(upload_to=casefile_location, help_text='The file path of the uploaded file, which is used to find the file name')
    case = models.ForeignKey('Case', on_delete=models.PROTECT, related_name='casefiles', help_text='A foreign key integer value identifying the case')
    from_requester = models.BooleanField(default=False, help_text='A boolean value indicating if the file is from the requester')
    final_letter = models.BooleanField(default=False, help_text='A boolean value indicating if the file is the final letter')
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True,
                                 related_name="casefiles", help_text='A foreign key integer value identifying the user uploading the file')
    uploaded_date = models.DateField(auto_now_add=True, null=True, blank=True, help_text='The date the file was uploaded in "YYYY-MM-DD" format')

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
    legal_description = models.CharField(max_length=255, blank=True, help_text='The legal description of the property')
    subdivision = models.CharField(max_length=255, blank=True, help_text='The subdivision name of the property')
    policy_number = models.CharField(max_length=255, blank=True, help_text='The policy number of the property')

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

    salutation = models.CharField(max_length=16, blank=True, help_text='Preferred salutation of the requester (e.g. Mrs.)')
    first_name = models.CharField(max_length=255, blank=True, help_text="Requester's first name")
    last_name = models.CharField(max_length=255, blank=True, help_text="Requester's last name")
    organization = models.CharField(max_length=255, blank=True, help_text="Requester's organization")
    email = models.CharField(max_length=255, blank=True, validators=[validators.EmailValidator], help_text="Requester's email")

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

    case = models.ForeignKey('Case', on_delete=models.CASCADE, help_text='A foreign key integer value identifying a case')
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE, help_text='A foreign key integer value identifying a tag')

    def __str__(self):
        return str(self.case) + " - " + str(self.tag)

    class Meta:
        db_table = "cbrs_casetag"
        unique_together = ("case", "tag")


class Tag(HistoryModel):
    """
    Terms or keywords used to describe, categorize, or group similar Cases for easier searching and reporting.
    """

    name = models.CharField(max_length=255, unique=True, help_text='The tag name')
    description = models.TextField(blank=True, help_text='A description of the tag')

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

    comment = models.TextField(help_text='A comment about a case')
    acase = models.ForeignKey('Case', on_delete=models.CASCADE, related_name='comments', help_text='A foreign key integer value identifying a case')

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

    determination = models.CharField(max_length=32, unique=True, help_text='Indicates the determination value ("In", "Out", etc.)')
    description = models.TextField(blank=True, help_text='A description of the determination value')

    def __str__(self):
        return self.determination

    class Meta:
        db_table = "cbrs_determination"


class SystemUnit(HistoryModel):
    """
    Lookup table for CBRS System Units.
    """

    system_unit_number = models.CharField(max_length=16, unique=True, help_text='The alphanumeric system unit number (e.g. A1)')
    system_unit_name = models.CharField(max_length=255, blank=True, help_text='The system unit name')
    system_unit_type = models.ForeignKey('SystemUnitType', on_delete=models.PROTECT, help_text='A foreign key integer value identifying the system unit type')
    field_office = models.ForeignKey('FieldOffice', on_delete=models.PROTECT,
                                     related_name='system_units', null=True, blank=True, help_text='A foreign key integer value identifying a field office')
    system_maps = models.ManyToManyField('SystemMap', through='SystemUnitMap', related_name='system_units',
                                        help_text='A many to many relationship of system maps based on a foreign key integer value identifying a system map')

    def __str__(self):
        return self.system_unit_number

    class Meta:
        db_table = "cbrs_systemunit"
        ordering = ['system_unit_number']


class SystemUnitType(HistoryModel):
    """
    Lookup table for Types for System Units.
    """

    unit_type = models.CharField(max_length=16, unique=True, help_text='An abbreviation of the system unit type (e.g. CBRS or OPA)')

    def __str__(self):
        return self.unit_type

    class Meta:
        db_table = "cbrs_systemunittype"
        ordering = ['unit_type']


class SystemUnitProhibitionDate(HistoryModel):
    """
    Lookup table for Prohibition Dates for System Units.
    """

    prohibition_date = models.DateField(help_text='The flood insurance prohibition date in "YYYY-MM-DD" format')
    system_unit = models.ForeignKey('SystemUnit', on_delete=models.CASCADE, related_name='prohibition_dates', help_text='A foreign key integer value identifying a system unit the prohibition was placed on')

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

    system_unit = models.ForeignKey('SystemUnit', on_delete=models.CASCADE, help_text='A foreign key integer value identifying a system unit')
    system_map = models.ForeignKey('SystemMap', on_delete=models.CASCADE, help_text='A foreign key integer value identifying a system map')

    def __str__(self):
        return str(self.system_unit) + " - " + str(self.system_map)

    class Meta:
        db_table = "cbrs_systemunitmap"
        unique_together = ("system_unit", "system_map")


class SystemMap(HistoryModel):
    """
    Lookup table for Maps for System Units.
    """

    map_number = models.CharField(max_length=16, help_text='The system map number')
    map_title = models.CharField(max_length=255, blank=True, help_text='The title of the system map')
    map_date = models.DateField(help_text='The system map date in "YYYY-MM-DD" format')
    effective = models.BooleanField(default=True, help_text='A boolean value indicating if the map is effective')

    def __str__(self):
        return self.map_number

    class Meta:
        db_table = "cbrs_systemmap"
        unique_together = ("map_number", "map_date")


class FieldOffice(HistoryModel):
    """
    Lookup table for Field Offices for System Units.
    """

    field_office_number = models.CharField(max_length=16, unique=True, help_text='A number indicating the id of the field office')
    field_office_name = models.CharField(max_length=255, blank=True, help_text='The name of the field office')
    field_agent_name = models.CharField(max_length=255, blank=True, help_text='The name of the agent representing the field office')
    field_agent_email = models.CharField(max_length=255, blank=True, validators=[validators.EmailValidator], help_text="The field office agent's email")
    city = models.CharField(max_length=255, blank=True, help_text='The city where the field office is located')
    state = USStateField(null=True, blank=True, help_text='The state in which the field office is located')

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
