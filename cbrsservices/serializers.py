import platform
import magic
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from rest_framework import serializers
from cbrsservices.models import *


######
#
#  Determinations
#
######


class CaseFileSerializer(serializers.ModelSerializer):

    def validate(self, data):
        file = self.initial_data.get('file', None)
        if file is not None:
            # check the file type, but don't trust the request's Content-Type since it's easy to spoof, instead
            # use python-magic (https://github.com/ahupp/python-magic and https://pypi.python.org/pypi/python-magic/)
            # which identifies file types by checking their headers according to a predefined list of file types.
            # we need to test for the host platform before we can initialize the Magic reader, since python-magic
            # must be manually configured on Windows after installation, but is automatically added to the system path
            # on Linux during installation; the magic_file shouldn't need to be explicitly referenced on Linux
            filemagic = None
            if platform.system() == 'Windows':
                magic_file = "D:\software\libmagicwin64\magic.mgc"
                filemagic = magic.Magic(magic_file=magic_file, mime=True)
            else:
                filemagic = magic.Magic(mime=True)
            filetype = filemagic.from_buffer(file.read())
            if filetype in settings.CONTENT_TYPES:
                # check the file size
                if int(file.size) > int(settings.MAX_UPLOAD_SIZE):
                    raise serializers.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (
                        filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(file.size)))
                else:
                    return data
            else:
                raise serializers.ValidationError(_('File type is not supported'))
        return data

    class Meta:
        model = CaseFile
        fields = ('id', 'name', 'file', 'case', 'from_requester', 'final_letter', 'uploaded_date',)
        read_only_fields = ('name',)


class CaseSerializer(serializers.ModelSerializer):

    def validate(self, data):
        """
        Ensure that no user is used by more than one of the following fields: Analyst, QC_Reviewer, FWS_Reviewer
        Also ensure that no date field is out of chronological order
        (dates must be in this order: request <= field office <= hq <= analyst <= qc <= fws <= final letter <= close)
        """
        an = self.initial_data.get('analyst', None)
        qc = self.initial_data.get('qc_reviewer', None)
        fws = self.initial_data.get('fws_reviewer', None)
        rdate = self.initial_data.get('request_date', None)
        fodate = self.initial_data.get('fws_fo_received_date', None)
        hqdate = self.initial_data.get('fws_hq_received_date', None)
        andate = self.initial_data.get('analyst_signoff_date', None)
        qcdate = self.initial_data.get('qc_reviewer_signoff_date', None)
        fldate = self.initial_data.get('final_letter_date', None)
        cdate = self.initial_data.get('close_date', None)
        if an is not None and qc is not None and an == qc:
            raise serializers.ValidationError("analyst cannot be the same as qc_reviewer")
        if an is not None and fws is not None and an == fws:
            raise serializers.ValidationError("analyst cannot be the same as fws_reviewer")
        if qc is not None and fws is not None and qc == fws:
            raise serializers.ValidationError("qc_reviewer cannot be the same as fws_reviewer")
        if rdate is not None and fodate is not None and rdate > fodate:
            raise serializers.ValidationError("request_date must be earlier than all other dates.")
        if fodate is not None and hqdate is not None and fodate > hqdate:
            raise serializers.ValidationError("fws_fo_received_date cannot be later than fws_hq_received_date.")
        if hqdate is not None and andate is not None and hqdate > andate:
            raise serializers.ValidationError("fws_hq_received_date cannot be later than analyst_signoff_date.")
        if andate is not None and qcdate is not None and andate > qcdate:
            raise serializers.ValidationError("analyst_signoff_date cannot be later than qc_reviewer_signoff_date.")
        if qcdate is not None and fldate is not None and qcdate > fldate:
            raise serializers.ValidationError("qc_reviewer_signoff_date cannot be later than final_letter_date.")
        if fldate is not None and cdate is not None and fldate > cdate:
            raise serializers.ValidationError("final_letter_date cannot be later than close_date.")
        return data

    analyst_string = serializers.StringRelatedField(source='analyst')
    qc_reviewer_string = serializers.StringRelatedField(source='qc_reviewer')
    cbrs_unit_string = serializers.StringRelatedField(source='cbrs_unit')
    map_number_string = serializers.StringRelatedField(source='map_number')
    determination_string = serializers.StringRelatedField(source='determination')

    class Meta:
        model = Case
        fields = ('id', 'case_number', 'case_reference', 'duplicate', 'status', 'request_date', 'requester', 'property',
                  'cbrs_unit', 'cbrs_unit_string', 'map_number', 'map_number_string', 'cbrs_map_date',
                  'determination', 'determination_string', 'prohibition_date', 'distance', 'fws_fo_received_date',
                  'fws_hq_received_date', 'final_letter_date', 'close_date', 'final_letter_recipient', 'analyst',
                  'analyst_string', 'analyst_signoff_date', 'qc_reviewer', 'qc_reviewer_string',
                  'qc_reviewer_signoff_date',
                  'priority', 'on_hold', 'invalid', 'comments', 'tags', 'case_files', 'created_by', 'modified_by',)
        read_only_fields = ('case_number', 'status', 'comments', 'tags', 'case_files',)


class WorkbenchSerializer(serializers.ModelSerializer):
    analyst_string = serializers.StringRelatedField(source='analyst')
    qc_reviewer_string = serializers.StringRelatedField(source='qc_reviewer')
    cbrs_unit_string = serializers.StringRelatedField(source='cbrs_unit')
    property_string = serializers.StringRelatedField(source='property')

    class Meta:
        model = Case
        fields = ('id', 'case_reference', 'status', 'request_date', 'property_string', 'cbrs_unit_string',
                  'distance', 'analyst_string', 'qc_reviewer_string', 'priority', 'on_hold', 'invalid', 'duplicate',)


class LetterSerializer(serializers.ModelSerializer):
    cbrs_unit_string = serializers.StringRelatedField(source='cbrs_unit')
    system_unit_type = serializers.StringRelatedField(source='cbrs_unit.system_unit_type')
    determination_string = serializers.StringRelatedField(source='determination')
    map_number_string = serializers.StringRelatedField(source='map_number')
    policy_number = serializers.CharField(source='property.policy_number')
    property_street = serializers.CharField(source='property.street')
    property_unit = serializers.CharField(source='property.unit')
    property_city = serializers.CharField(source='property.city')
    property_state = serializers.CharField(source='property.state')
    property_zipcode = serializers.CharField(source='property.zipcode')
    legal_description = serializers.CharField(source='property.legal_description')
    subdivision = serializers.CharField(source='property.subdivision')
    salutation = serializers.CharField(source='requester.salutation')
    first_name = serializers.CharField(source='requester.first_name')
    last_name = serializers.CharField(source='requester.last_name')
    requester_organization = serializers.CharField(source='requester.organization')
    requester_street = serializers.CharField(source='requester.street')
    requester_unit = serializers.CharField(source='requester.unit')
    requester_city = serializers.CharField(source='requester.city')
    requester_state = serializers.CharField(source='requester.state')
    requester_zipcode = serializers.CharField(source='requester.zipcode')

    class Meta:
        model = Case
        fields = ('id', 'case_reference', 'request_date', 'determination', 'determination_string', 'cbrs_unit',
                  'cbrs_unit_string', 'system_unit_type', 'prohibition_date', 'map_number', 'map_number_string',
                  'cbrs_map_date', 'final_letter_recipient', 'policy_number', 'property_street', 'property_unit',
                  'property_city', 'property_state', 'property_zipcode', 'legal_description', 'subdivision',
                  'salutation', 'first_name', 'last_name', 'requester_organization', 'requester_street',
                  'requester_unit', 'requester_city', 'requester_state', 'requester_zipcode', )


class CaseIDSerializer(serializers.ModelSerializer):

    class Meta:
        model = Case
        fields = ('id', 'case_reference', 'duplicate')


class PropertySerializer(serializers.ModelSerializer):

    class Meta:
        model = Property
        fields = ('id', 'street', 'unit', 'city', 'state', 'zipcode', 'subdivision', 'legal_description',
                  'policy_number', 'cases',)
        read_only_fields = ('cases',)


class RequesterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Requester
        fields = ('id', 'salutation', 'first_name', 'last_name', 'organization', 'email',
                  'street', 'unit', 'city', 'state', 'zipcode', 'cases',)
        read_only_fields = ('cases',)


######
#
#  Tags
#
######


class CaseTagSerializer(serializers.ModelSerializer):
    tagname = serializers.StringRelatedField(source='tag')

    class Meta:
        model = CaseTag
        fields = ('id', 'case', 'tag', 'tagname',)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'description',)


######
#
#  Comments
#
######


class CommentSerializer(serializers.ModelSerializer):
    created_by_string = serializers.StringRelatedField(source='created_by')

    class Meta:
        model = Comment
        fields = ('id', 'comment', 'acase', 'created_by', 'created_by_string', 'created_date',)
        read_only_fields = ('created_by_string', 'created_date',)


######
#
#  Lookup Tables
#
######


class DeterminationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Determination
        fields = ('id', 'determination', 'description',)


class SystemUnitSerializer(serializers.ModelSerializer):

    class Meta:
        model = SystemUnit
        fields = ('id', 'system_unit_number', 'system_unit_name', 'field_office', 'system_maps',)
        read_only_fields = ('system_maps',)


class SystemUnitProhibitionDateSerializer(serializers.ModelSerializer):
    prohibition_date_mdy = serializers.DateField(format='%m/%d/%Y', source='prohibition_date')

    class Meta:
        model = SystemUnitProhibitionDate
        fields = ('id', 'prohibition_date', 'prohibition_date_mdy', 'system_unit',)


class SystemUnitMapSerializer(serializers.ModelSerializer):

    class Meta:
        model = SystemUnitMap
        fields = ('id', 'system_unit', 'system_map',)


class SystemMapSerializer(serializers.ModelSerializer):

    class Meta:
        model = SystemMap
        fields = ('id', 'map_number', 'map_title', 'map_date', 'effective', 'system_units')
        read_only_fields = ('system_units',)


class FieldOfficeSerializer(serializers.ModelSerializer):

    class Meta:
        model = FieldOffice
        fields = ('id', 'field_office_number', 'field_office_name', 'field_agent_name', 'field_agent_email',
                  'city', 'state',)


######
#
#  Reports
#
######


class ReportSerializer(serializers.ModelSerializer):
    property_string = serializers.StringRelatedField(source='property')
    determination_string = serializers.StringRelatedField(source='determination')

    class Meta:
        model = ReportCase
        fields = ('id', 'status', 'request_date', 'close_date', 'property_string', 'determination_string',)


class ReportCasesByUnitSerializer(serializers.ModelSerializer):
    def get_street_address(self, obj):
        prop = obj.property
        prop_street = Property.objects.filter(id=prop.id).values_list('street', flat=True)[0]
        prop_street_address = prop_street.split(",")[0]
        return prop_street_address

    cbrs_unit_string = serializers.StringRelatedField(source='cbrs_unit')
    property_string = serializers.StringRelatedField(source='property')
    determination_string = serializers.StringRelatedField(source='determination')
    street_address = serializers.SerializerMethodField()

    class Meta:
        model = ReportCase
        fields = ('id', 'status', 'prohibition_date', 'cbrs_unit_string', 'request_date', 'property_string',
                  'determination_string', 'street_address')


class ReportDaysToResolutionSerializer(serializers.ModelSerializer):
    property_string = serializers.StringRelatedField(source='property')
    determination_string = serializers.StringRelatedField(source='determination')

    class Meta:
        model = ReportCase
        fields = ('id', 'case_reference', 'request_date', 'final_letter_date', 'close_date', 'close_days',
                  'property_string', 'determination_string',)


class ReportDaysToEachStatusSerializer(serializers.ModelSerializer):
    property_string = serializers.StringRelatedField(source='property')
    determination_string = serializers.StringRelatedField(source='determination')

    class Meta:
        model = ReportCase
        fields = ('id', 'case_reference', 'status', 'request_date', 'analyst_signoff_date', 'qc_reviewer_signoff_date',
                  'final_letter_date', 'close_date', 'close_days', 'analyst_days', 'qc_reviewer_days',
                  'final_letter_days', 'property_string', 'determination_string',)


class ReportCountOfCasesByStatusSerializer(serializers.Serializer):
    count_received = serializers.IntegerField()
    count_awaiting_qc = serializers.IntegerField()
    count_awaiting_final_letter = serializers.IntegerField()
    count_closed = serializers.IntegerField()
    count_closed_no_final_letter = serializers.IntegerField()


######
#
#  Users
#
######


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email',
                  'groups', 'user_permissions', 'is_superuser', 'is_staff', 'is_active',)
