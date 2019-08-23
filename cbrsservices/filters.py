from django_filters.rest_framework import DjangoFilterBackend, FilterSet, NumberFilter, CharFilter, BooleanFilter, ModelMultipleChoiceFilter
from cbrsservices.models import *
from cbrsservices.field_descriptions import *


# TODO: edit field descriptions of items that allow multiple inputs via comma separated lists (e.g. case_number), can't have spaces
# Also, if Aaron gives the go-ahead, we can remove a lot of the filtering done in the get_queryset method, because we're doing that here by
# specifying what the lookup_exr and field_names are, e.g. BooleanFilter(field_name='priority', lookup_expr='exact') does the same as
# queryset.filter(priority__exact=priority) and we can also create methods for more complex filters or those that aren't model fields
class CaseFilter(FilterSet):
    format = CharFilter(method='nonModelValue', label=queryparams.format)
    view = CharFilter(method='nonModelValue', label=queryparams.view)
    case_reference = CharFilter(method='nonModelValue', label=case.case_reference)
    property = CharFilter(method='nonModelValue', label=case.property)
    requester = CharFilter(method='nonModelValue', label=case.requester)
    status = CharFilter(method='nonModelValue', label=case.status)
    case_number = CharFilter(method='nonModelValue', label=case.case_number)
    request_date_after = CharFilter(method='nonModelValue', label=queryparams.request_date_after)
    request_date_before = CharFilter(method='nonModelValue', label=queryparams.request_date_before)
    distance_from = NumberFilter(method='nonModelValue', label=queryparams.distance_from)
    distance_to = NumberFilter(method='nonModelValue', label=queryparams.distance_to)
    analyst = CharFilter(field_name='analyst', lookup_expr='exact', label=case.analyst)
    qc_reviewer = CharFilter(field_name='qc_reviewer', lookup_expr='exact', label=case.qc_reviewer)
    cbrs_unit = CharFilter(field_name='cbrs_unit', lookup_expr='exact', label=case.cbrs_unit)
    street = CharFilter(method='nonModelValue', label=address.street)
    city = CharFilter(method='nonModelValue', label=address.city)
    policy_number = CharFilter(field_name='policy_number', lookup_expr='in', label=address.policy_number)
    tags = CharFilter(field_name='tags', lookup_expr='exact', label=case.tags)
    priority = BooleanFilter(field_name='priority', lookup_expr='exact', label=case.priority)
    on_hold = BooleanFilter(field_name='on_hold', lookup_expr='exact', label=case.on_hold)
    invalid = BooleanFilter(field_name='invalid', lookup_expr='exact', label=case.invalid)
    hard_copy_map_reviewed = BooleanFilter(field_name='hard_copy_map_reviewed', lookup_expr='exact', label=case.hard_copy_map_reviewed)
    duplicate = CharFilter(field_name='duplicate', lookup_expr='exact', label=case.duplicate)
    fiscal_year = CharFilter(method='nonModelValue', label=queryparams.fiscal_year)
    freetext = CharFilter(method='nonModelValue', label=queryparams.freetext)


    def nonModelValue(self, queryset, value, *args):
        return queryset

    class Meta:
        model = Case
        fields = ['format', 'view', 'case_reference', 'property', 'requester', 'status', 'case_number', 'request_date_after', 'request_date_before',
            'distance_from', 'distance_to', 'analyst', 'qc_reviewer', 'cbrs_unit', 'street', 'city', 'policy_number', 'tags',
            'priority', 'on_hold', 'invalid', 'hard_copy_map_reviewed', 'duplicate', 'fiscal_year', 'freetext']

class CaseFileFilter(FilterSet):
    case = NumberFilter(field_name='case', lookup_expr='exact', label=casefile.case)

    class Meta:
        model = CaseFile
        fields = ['case']

class PropertyFilter(FilterSet):
    case = NumberFilter(method='nonModelValue', label=queryparams.case)
    street = CharFilter(field_name='street', lookup_expr='exact', label=address.street)
    unit = CharFilter(field_name='unit', lookup_expr='exact', label=address.unit)
    city = CharFilter(field_name='city', lookup_expr='exact', label=address.city)
    state = CharFilter(field_name='state', lookup_expr='exact', label=address.state)
    zipcode = CharFilter(field_name='zipcode', lookup_expr='exact', label=address.zipcode)
    legal_description = CharFilter(field_name='legal_description', lookup_expr='exact', label=address.legal_description)

    def nonModelValue(self, queryset, value, *args):
        return queryset

    class Meta:
        model = Property
        fields = ['case', 'street', 'unit', 'city', 'state', 'zipcode', 'legal_description']


class RequesterFilter(FilterSet):
    case = NumberFilter(method='nonModelValue', label=queryparams.case)
    salutation = CharFilter(field_name='salutation', lookup_expr='exact', label=requester.salutation)
    first_name = CharFilter(field_name='first_name', lookup_expr='exact', label=requester.first_name)
    last_name = CharFilter(field_name='last_name', lookup_expr='exact', label=requester.last_name)
    organization = CharFilter(field_name='organization', lookup_expr='exact', label=requester.organization)
    email = CharFilter(field_name='email', lookup_expr='exact', label=requester.email)
    street = CharFilter(field_name='street', lookup_expr='exact', label=address.street)
    unit = CharFilter(field_name='unit', lookup_expr='exact', label=address.unit)
    city = CharFilter(field_name='city', lookup_expr='exact', label=address.city)
    state = CharFilter(field_name='state', lookup_expr='exact', label=address.state)
    zipcode = CharFilter(field_name='zipcode', lookup_expr='exact', label=address.zipcode)

    def nonModelValue(self, queryset, value, *args):
        return queryset

    class Meta:
        model = Requester
        fields = ['case', 'salutation', 'first_name', 'last_name', 'organization', 'email', 'street', 'unit', 'city', 'state', 'zipcode']


class CaseTagFilter(FilterSet):
    case = NumberFilter(field_name='case', lookup_expr='exact', label=queryparams.case)

    class Meta:
        model = CaseTag
        fields = ['case']

class TagFilter(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='exact', label=casetag.name)

    class Meta:
        model = Tag
        fields = ['name']

class CommentFilter(FilterSet):
    case = NumberFilter(method='nonModelValue', label=queryparams.case)

    def nonModelValue(self, queryset, value, *args):
        return queryset

    class Meta:
        model = Comment
        fields = ['case']

class DeterminationFilter(FilterSet):

    class Meta:
        model = Determination
        fields = []

class SystemUnitFilter(FilterSet):
    freetext = CharFilter(method='nonModelValue', label=queryparams.freetext)

    def nonModelValue(self, queryset, value, *args):
        return queryset

    class Meta:
        model = SystemUnit
        fields = ['freetext']

class SystemUnitProhibitionDateFilter(FilterSet):
    unit = NumberFilter(method='nonModelValue', label=prohibitiondate.system_unit)
    freetext = CharFilter(method='nonModelValue', label=queryparams.freetext)

    def nonModelValue(self, queryset, value, *args):
        return queryset

    class Meta:
        model = SystemUnitProhibitionDate
        fields = ['unit', 'freetext']

class SystemUnitMapFilter(FilterSet):
    unit = NumberFilter(method='nonModelValue', label=systemunitmap.system_unit)
    map = NumberFilter(method='nonModelValue', label=systemunitmap.system_map)

    def nonModelValue(self, queryset, value, *args):
        return queryset

    class Meta:
        model = SystemUnitMap
        fields = ['unit', 'map']

class SystemMapFilter(FilterSet):
    unit = NumberFilter(method='nonModelValue', label=systemunitmap.system_unit)
    freetext = CharFilter(method='nonModelValue', label=queryparams.freetext)

    def nonModelValue(self, queryset, value, *args):
        return queryset

    class Meta:
        model = SystemMap
        fields = ['unit', 'freetext']


class ReportCaseFilter(FilterSet):
    format = CharFilter(method='nonModelValue', label=queryparams.format)
    report = CharFilter(field_name='report', lookup_expr='exact', label=queryparams.report)
    cbrs_unit = NumberFilter(field_name='cbrs_unit', lookup_expr='exact', label=case.cbrs_unit)
    user = CharFilter(field_name='user', lookup_expr='exact', label=queryparams.user)

    def nonModelValue(self, queryset, value, *args):
        return queryset

    class Meta:
        model = ReportCase
        fields = ['format', 'report', 'cbrs_unit', 'user']

class ReportCaseCountFilter(FilterSet):
    format = CharFilter(method='nonModelValue', label=queryparams.format)

    def nonModelValue(self, queryset, value, *args):
        return queryset

    class Meta:
        model = ReportCase
        fields = ['format']

class UserFilter(FilterSet):
    username = CharFilter(field_name='username', lookup_expr='exact', label=user.username)
    is_active = BooleanFilter(field_name='is_active', lookup_expr='exact', label=user.is_active)
    used_users = CharFilter(method='nonModelValue', label=queryparams.used_users)
    freetext = CharFilter(method='nonModelValue', label=queryparams.freetext)

    def nonModelValue(self, queryset, value, *args):
        return queryset

    class Meta:
        model = User
        fields = ['username', 'is_active', 'used_users', 'freetext']
