import platform
from rest_framework import serializers
from cbraservices.models import *


######
#
#  Determinations
#
######


class CaseFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CaseFile
        fields = ('id', 'name', 'file', 'case', 'uploaded_date',)
        read_only_fields = ('name',)


class CaseSerializer(serializers.ModelSerializer):

    def validate(self, data):
        """
        Ensure that no user is used by more than one of the following fields: Analyst, QC_Reviewer, FWS_Reviewer
        """
        an = self.initial_data.get('analyst', None)
        qc = self.initial_data.get('qc_reviewer', None)
        fws = self.initial_data.get('fws_reviewer', None)
        if an is not None and qc is not None and an == qc:
            raise serializers.ValidationError("analyst cannot be the same as qc_reviewer")
        if an is not None and fws is not None and an == fws:
            raise serializers.ValidationError("analyst cannot be the same as fws_reviewer")
        if qc is not None and fws is not None and qc == fws:
            raise serializers.ValidationError("qc_reviewer cannot be the same as fws_reviewer")
        return data

    analyst_string = serializers.StringRelatedField(source='analyst')
    qc_reviewer_string = serializers.StringRelatedField(source='qc_reviewer')
    fws_reviewer_string = serializers.StringRelatedField(source='fws_reviewer')
    cbrs_unit_string = serializers.StringRelatedField(source='cbrs_unit')
    map_number_string = serializers.StringRelatedField(source='map_number')
    determination_string = serializers.StringRelatedField(source='determination')

    class Meta:
        model = Case
        fields = ('id', 'case_number', 'case_hash', 'status', 'request_date', 'requester', 'property', 'cbrs_unit',
                  'cbrs_unit_string', 'map_number', 'map_number_string', 'cbrs_map_date', 'determination',
                  'determination_string', 'prohibition_date', 'distance', 'fws_fo_received_date',
                  'fws_hq_received_date', 'final_letter_date', 'close_date', 'final_letter_recipient', 'analyst',
                  'analyst_string', 'analyst_signoff_date', 'qc_reviewer', 'qc_reviewer_string',
                  'qc_reviewer_signoff_date', 'fws_reviewer', 'fws_reviewer_string', 'fws_reviewer_signoff_date',
                  'priority', 'comments', 'tags', 'case_files', 'created_by', 'modified_by',)
        read_only_fields = ('case_number', 'status', 'comments', 'tags', 'case_files',)


class WorkbenchSerializer(serializers.ModelSerializer):
    analyst_string = serializers.StringRelatedField(source='analyst')
    qc_reviewer_string = serializers.StringRelatedField(source='qc_reviewer')
    cbrs_unit_string = serializers.StringRelatedField(source='cbrs_unit')
    property_string = serializers.StringRelatedField(source='property')

    class Meta:
        model = Case
        fields = ('id', 'status', 'request_date', 'property_string', 'cbrs_unit_string', 'distance',
                  'analyst_string', 'qc_reviewer_string', 'priority',)


class PropertySerializer(serializers.ModelSerializer):

    class Meta:
        model = Property
        fields = ('id', 'street', 'unit', 'city', 'state', 'zipcode', 'subdivision', 'policy_number', 'cases')
        read_only_fields = ('cases',)


class RequesterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Requester
        fields = ('id', 'salutation', 'first_name', 'last_name', 'organization', 'email',
                  'street', 'unit', 'city', 'state', 'zipcode', 'cases')
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
        fields = ('id', 'case', 'tag', 'tagname')


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

    class Meta:
        model = Comment
        fields = ('id', 'comment', 'case',)


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

    class Meta:
        model = SystemUnitProhibitionDate
        fields = ('id', 'prohibition_date', 'system_unit',)


class SystemUnitMapSerializer(serializers.ModelSerializer):

    class Meta:
        model = SystemUnitMap
        fields = ('id', 'system_unit', 'system_map',)


class SystemMapSerializer(serializers.ModelSerializer):

    class Meta:
        model = SystemMap
        fields = ('id', 'map_number', 'map_title', 'map_date',)


class FieldOfficeSerializer(serializers.ModelSerializer):

    class Meta:
        model = FieldOffice
        fields = ('id', 'field_office_number', 'field_office_name', 'field_agent_name', 'field_agent_email',
                  'city', 'state',)


######
#
#  Users
#
######


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email',
                  'groups', 'user_permissions', 'is_superuser', 'is_staff', 'is_active')
