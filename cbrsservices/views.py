from itertools import chain
from datetime import datetime as dt
from django.db.models import Q
from rest_framework import views, viewsets, generics, authentication
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.parsers import FormParser, MultiPartParser
from cbrsservices.serializers import *
from cbrsservices.models import *
from cbrsservices.permissions import *
from cbrsservices.renderers import *
from cbrsservices.paginations import *


########################################################################################################################
#
#  copyright: 2016 WiM - USGS
#  authors: Aaron Stephenson USGS WiM (Web Informatics and Mapping)
#
#  In Django, a view is what takes a Web request and returns a Web response. The response can be many things, but most
#  of the time it will be a Web page, a redirect, or a document. In this case, the response will almost always be data
#  in JSON format.
#
#  All these views are written as Class-Based Views (https://docs.djangoproject.com/en/1.8/topics/class-based-views/)
#  because that is the paradigm used by Django Rest Framework (http://www.django-rest-framework.org/api-guide/views/)
#  which is the toolkit we used to create web services in Django.
#
#
########################################################################################################################


######
#
#  Abstract Base Classes
#
######


class HistoryViewSet(viewsets.ModelViewSet):
    """
    This class will automatically assign the User ID to the created_by and modified_by history fields when appropriate
    """

    permission_classes = (IsActive,)

    def perform_create(self, serializer):
        if self.basename != 'users':
            serializer.save(created_by=self.request.user, modified_by=self.request.user)
        else:
            serializer.save()

    def perform_update(self, serializer):
        if self.basename != 'users':
            serializer.save(modified_by=self.request.user)
        else:
            serializer.save()


######
#
#  Determinations
#
######


class CaseViewSet(HistoryViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    @action(methods=['post'], detail=True)
    def send_final_email(self, request, pk=None):
        case = self.get_object()
        case.send_final_email()
        return Response({'status': 'final email sent'})

    # override the default renderers to use a custom DOCX renderer when requested
    def get_renderers(self):
        frmt = self.request.query_params.get('format', None) if self.request else None
        if frmt is not None and frmt == 'docx':
            renderer_classes = (FinalLetterDOCXRenderer,) + tuple(api_settings.DEFAULT_RENDERER_CLASSES)
        else:
            renderer_classes = tuple(api_settings.DEFAULT_RENDERER_CLASSES)
        return [renderer_class() for renderer_class in renderer_classes]

    # override the default serializer_class if workbench or report format is specified
    def get_serializer_class(self):
        view = self.request.query_params.get('view', None) if self.request else None
        # if view is not specified or not equal to workbench or report, assume case
        if view is not None and view == 'workbench':
            return WorkbenchSerializer
        elif view is not None and view == 'report':
            return ReportSerializer
        elif view is not None and self.request.accepted_renderer.format == 'docx':
            return LetterSerializer
        elif view is not None and view == 'caseid':
            return CaseIDSerializer
        else:
            return CaseSerializer

    # override the default finalize_response to assign a filename to DOCX files
    # see https://github.com/mjumbewu/django-rest-framework-csv/issues/15
    def finalize_response(self, request, *args, **kwargs):
        response = super(viewsets.ModelViewSet, self).finalize_response(request, *args, **kwargs)
        if request is not None and request.accepted_renderer.format == 'docx':
            filename = 'final_letter_case_'
            filename += self.get_queryset().first().case_reference + '_'
            filename += dt.now().strftime("%Y") + '-' + dt.now().strftime("%m") + '-' + dt.now().strftime("%d")
            filename += '.docx'
            response['Content-Disposition'] = "attachment; filename=%s" % filename
            response['Access-Control-Expose-Headers'] = 'Content-Disposition'
        return response

    # override the default queryset to allow filtering by URL arguments
    def get_queryset(self):
        queryset = Case.objects.all()
        if self.request:
            # filter by case reference, exact
            case_reference = self.request.query_params.get('case_reference', None)
            if case_reference is not None:
                queryset = queryset.filter(case_reference__exact=case_reference)
            # filter by property ID, exact
            property = self.request.query_params.get('property', None)
            if property is not None:
                queryset = queryset.filter(property__exact=property)
            # filter by requester ID, exact
            requester = self.request.query_params.get('requester', None)
            if requester is not None:
                queryset = queryset.filter(requester__exact=requester)
            # filter by status, exact
            status = self.request.query_params.get('status', None)
            if status is not None:
                if status == 'Closed with no Final Letter':
                    queryset = queryset.filter(close_date__isnull=False,
                                               final_letter_date__isnull=True)
                elif status == 'Final':
                    queryset = queryset.filter(close_date__isnull=False,
                                               final_letter_date__isnull=False)
                elif status == 'Awaiting Final Letter':
                    queryset = queryset.filter(qc_reviewer_signoff_date__isnull=False,
                                               close_date__isnull=True,
                                               final_letter_date__isnull=True)
                elif status == 'Awaiting QC':
                    queryset = queryset.filter(analyst_signoff_date__isnull=False,
                                               qc_reviewer_signoff_date__isnull=True,
                                               close_date__isnull=True,
                                               final_letter_date__isnull=True)
                elif status == 'Received':
                    queryset = queryset.filter(analyst_signoff_date__isnull=True,
                                               qc_reviewer_signoff_date__isnull=True,
                                               close_date__isnull=True,
                                               final_letter_date__isnull=True)
                elif status == 'Open':
                    queryset = queryset.filter(close_date__isnull=True,
                                               final_letter_date__isnull=True)
                else:
                    pass
            # filter by case number, exact list
            case_number = self.request.query_params.get('case_number', None)
            if case_number is not None:
                case_number_list = case_number.split(',')
                queryset = queryset.filter(id__in=case_number_list)
            # filter by case reference, exact list
            case_reference = self.request.query_params.get('case_reference', None)
            if case_reference is not None:
                case_reference_list = case_reference.split(',')
                queryset = queryset.filter(case_reference__in=case_reference_list)
            # filter by request date (after only, before only, or between both, depending on which URL params appear)
            request_date_after = self.request.query_params.get('request_date_after', None)
            request_date_before = self.request.query_params.get('request_date_before', None)
            if request_date_after is not None and request_date_before is not None:
                # the filter below using __range is date-inclusive
                # queryset = queryset.filter(request_date__range=(request_date_after, request_date_before))
                # the filter below is date-exclusive
                queryset = queryset.filter(request_date__gt=request_date_after, request_date__lt=request_date_before)
            elif request_date_after is not None:
                queryset = queryset.filter(request_date__gt=request_date_after)
            elif request_date_before is not None:
                queryset = queryset.filter(request_date__lt=request_date_before)
            # filter by distance (to only, from only, or between both, depending on which URL params appear)
            distance_from = self.request.query_params.get('distance_from', None)
            distance_to = self.request.query_params.get('distance_to', None)
            if distance_from is not None and distance_to is not None:
                # the filter below using __range is value-inclusive
                # queryset = queryset.filter(distance__range=(distance_from, distance_to))
                # the filter below is value-exclusive
                queryset = queryset.filter(distance__gt=distance_from, distance__lt=distance_to)
            elif distance_from is not None:
                queryset = queryset.filter(distance__gt=distance_from)
            elif distance_to is not None:
                queryset = queryset.filter(distance__lt=distance_to)
            # filter by analyst IDs, exact list
            analyst = self.request.query_params.get('analyst', None)
            if analyst is not None:
                analyst_list = analyst.split(',')
                queryset = queryset.filter(analyst__in=analyst_list)
            # filter by QC reviewer IDs, exact list
            qc_reviewer = self.request.query_params.get('qc_reviewer', None)
            if qc_reviewer is not None:
                qc_reviewer_list = qc_reviewer.split(',')
                queryset = queryset.filter(qc_reviewer__in=qc_reviewer_list)
            # filter by CBRS unit IDs, exact list
            cbrs_unit = self.request.query_params.get('cbrs_unit', None)
            if cbrs_unit is not None:
                cbrs_unit_list = cbrs_unit.split(',')
                queryset = queryset.filter(cbrs_unit__in=cbrs_unit_list)
            # filter by street, case-insensitive contain
            street = self.request.query_params.get('street', None)
            if street is not None:
                queryset = queryset.filter(property__street__icontains=street)
            # filter by city, case-insensitive contain
            city = self.request.query_params.get('city', None)
            if city is not None:
                queryset = queryset.filter(property__city__icontains=city)
            # policy_number, exact list
            policy_number = self.request.query_params.get('policy_number', None)
            if policy_number is not None:
                policy_number_list = policy_number.split(',')
                queryset = queryset.filter(property__policy_number__in=policy_number_list)
            # filter by tag IDs, exact list
            tags = self.request.query_params.get('tags', None)
            if tags is not None:
                tag_list = tags.split(',')
                queryset = queryset.filter(tags__in=tag_list)
            # filter by priority, exact
            priority = self.request.query_params.get('priority', None)
            if priority is not None:
                queryset = queryset.filter(priority__exact=priority)
            # filter by on_hold, exact
            on_hold = self.request.query_params.get('on_hold', None)
            if on_hold is not None:
                queryset = queryset.filter(on_hold__exact=on_hold)
            # filter by invalid, exact
            invalid = self.request.query_params.get('invalid', None)
            if invalid is not None:
                queryset = queryset.filter(invalid__exact=invalid)
            # filter by hard_copy_map_reviewed, exact
            hard_copy_map_reviewed = self.request.query_params.get('hard_copy_map_reviewed', None)
            if hard_copy_map_reviewed is not None:
                queryset = queryset.filter(hard_copy_map_reviewed__exact=hard_copy_map_reviewed)
            # filter by duplicate, exact (also include the original case, per cooperator request)
            duplicate = self.request.query_params.get('duplicate', None)
            if duplicate is not None:
                if duplicate == 'none':
                    queryset = queryset.filter(duplicate__isnull=True)
                else:
                    queryset = queryset.filter(
                        Q(id__exact=duplicate) |
                        Q(duplicate__exact=duplicate))
            # filter by fiscal year, exact
            fiscal_year = self.request.query_params.get('fiscal_year', None)
            if fiscal_year is not None:
                fiscal_year_start = str(int(fiscal_year) - 1) + "-10-01"
                fiscal_year_end = fiscal_year + "-09-30"
                queryset = queryset.filter(request_date__gte=fiscal_year_start, request_date__lte=fiscal_year_end)
            # filter by freetext, case-insensitive contain
            freetext = self.request.query_params.get('freetext', None)
            if freetext is not None:
                queryset = queryset.filter(
                    Q(analyst__username__icontains=freetext) |
                    Q(analyst__first_name__icontains=freetext) |
                    Q(analyst__last_name__icontains=freetext) |
                    Q(case_reference__icontains=freetext) |
                    #Q(case_number__icontains=freetext) |
                    #Q(RawSQL("SELECT id FROM cbrs_case WHERE id::varchar ILIKE %s", freetext)) | #("'%'" + freetext + "'%'",))) |
                    Q(cbrs_unit__system_unit_name__icontains=freetext) |
                    Q(property__street__icontains=freetext) |
                    Q(property__unit__icontains=freetext) |
                    Q(property__city__icontains=freetext) |
                    Q(property__policy_number__icontains=freetext))
        return queryset


class CaseFileViewSet(HistoryViewSet):
    serializer_class = CaseFileSerializer
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser,)

    # override the default create to include user information
    def perform_create(self, serializer):

        def get_user():
            if self.request.user.is_anonymous():
                return None
            else:
                return self.request.user

        serializer.save(case=Case.objects.get(pk=int(self.request.data.get('case'))),
                        file=self.request.data.get('file'), uploader=get_user(),
                        created_by=get_user(), modified_by=get_user())

    # override the default queryset to allow filtering by URL arguments
    def get_queryset(self):
        queryset = CaseFile.objects.all()
        if self.request:
            # filter by case ID, exact
            case_id = self.request.query_params.get('case', None)
            if case_id is not None:
                queryset = queryset.filter(case__exact=case_id)
        return queryset


class PropertyViewSet(HistoryViewSet):
    serializer_class = PropertySerializer
    permission_classes = (permissions.IsAuthenticated,)

    # override the default queryset to allow filtering by URL arguments
    def get_queryset(self):
        queryset = Property.objects.all()
        if self.request:
            # filter by case ID, exact
            case_id = self.request.query_params.get('case', None)
            if case_id is not None:
                queryset = queryset.filter(cases__exact=case_id)
            # filter by street, exact
            street = self.request.query_params.get('street', None)
            if street is not None:
                queryset = queryset.filter(street__exact=street)
            # filter by unit, exact
            unit = self.request.query_params.get('unit', None)
            if unit is not None:
                queryset = queryset.filter(unit__exact=unit)
            # filter by city, exact
            city = self.request.query_params.get('city', None)
            if city is not None:
                queryset = queryset.filter(city__exact=city)
            # filter by state, exact
            state = self.request.query_params.get('state', None)
            if state is not None:
                queryset = queryset.filter(state__exact=state)
            # filter by zipcode, exact
            zipcode = self.request.query_params.get('zipcode', None)
            if zipcode is not None:
                queryset = queryset.filter(zipcode__exact=zipcode)
            # filter by legal_description, exact
            legal_description = self.request.query_params.get('legal_description', None)
            if legal_description is not None:
                queryset = queryset.filter(legal_description__exact=legal_description)
        return queryset


class RequesterViewSet(HistoryViewSet):
    serializer_class = RequesterSerializer
    permission_classes = (permissions.IsAuthenticated,)

    # override the default queryset to allow filtering by URL arguments
    def get_queryset(self):
        queryset = Requester.objects.all()
        if self.request:
            # filter by case ID, exact
            case_id = self.request.query_params.get('case', None)
            if case_id is not None:
                queryset = queryset.filter(cases__exact=case_id)
            # filter by salutation, exact
            salutation = self.request.query_params.get('salutation', None)
            if salutation is not None:
                queryset = queryset.filter(salutation__exact=salutation)
            # filter by first_name, exact
            first_name = self.request.query_params.get('first_name', None)
            if first_name is not None:
                queryset = queryset.filter(first_name__exact=first_name)
            # filter by last_name, exact
            last_name = self.request.query_params.get('last_name', None)
            if last_name is not None:
                queryset = queryset.filter(last_name__exact=last_name)
            # filter by organization, exact
            organization = self.request.query_params.get('organization', None)
            if organization is not None:
                queryset = queryset.filter(organization__exact=organization)
            # filter by email, exact
            email = self.request.query_params.get('email', None)
            if email is not None:
                queryset = queryset.filter(email__exact=email)
            # filter by street, exact
            street = self.request.query_params.get('street', None)
            if street is not None:
                queryset = queryset.filter(street__exact=street)
            # filter by unit, exact
            unit = self.request.query_params.get('unit', None)
            if unit is not None:
                queryset = queryset.filter(unit__exact=unit)
            # filter by city, exact
            city = self.request.query_params.get('city', None)
            if city is not None:
                queryset = queryset.filter(city__exact=city)
            # filter by state, exact
            state = self.request.query_params.get('state', None)
            if state is not None:
                queryset = queryset.filter(state__exact=state)
            # filter by zipcode, exact
            zipcode = self.request.query_params.get('zipcode', None)
            if zipcode is not None:
                queryset = queryset.filter(zipcode__exact=zipcode)
        return queryset


######
#
#  Tags
#
######


class CaseTagViewSet(HistoryViewSet):
    serializer_class = CaseTagSerializer
    permission_classes = (permissions.IsAuthenticated,)

    # override the default queryset to allow filtering by URL arguments
    def get_queryset(self):
        queryset = CaseTag.objects.all()
        if self.request:
            # filter by case ID, exact
            case_id = self.request.query_params.get('case', None)
            if case_id is not None:
                queryset = queryset.filter(case_id__exact=case_id)
        return queryset


class TagViewSet(HistoryViewSet):
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticated,)

    # override the default queryset to allow filtering by URL arguments
    def get_queryset(self):
        queryset = Tag.objects.all()
        if self.request:
            # filter by tag name, exact
            tag_name = self.request.query_params.get('name', None)
            if tag_name is not None:
                queryset = queryset.filter(name__exact=tag_name)
        return queryset


######
#
#  Comments
#
######


class CommentViewSet(HistoryViewSet):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    # override the default queryset to allow filtering by URL arguments
    def get_queryset(self):
        queryset = Comment.objects.all()
        if self.request:
            # filter by case ID, exact
            case_id = self.request.query_params.get('case', None)
            if case_id is not None:
                queryset = queryset.filter(acase_id__exact=case_id)
        return queryset


######
#
#  Lookup Tables
#
######


class DeterminationViewSet(HistoryViewSet):
    queryset = Determination.objects.all()
    serializer_class = DeterminationSerializer
    permission_classes = (permissions.IsAuthenticated,)


class SystemUnitViewSet(HistoryViewSet):
    serializer_class = SystemUnitSerializer
    permission_classes = (permissions.IsAuthenticated,)

    # override the default queryset to allow filtering by URL arguments
    def get_queryset(self):
        queryset = SystemUnit.objects.all()
        if self.request:
            # filter by freetext, case-insensitive contain
            freetext = self.request.query_params.get('freetext', None)
            if freetext is not None:
                queryset = queryset.filter(
                    Q(system_unit_number__icontains=freetext) |
                    Q(system_unit_name__icontains=freetext) |
                    Q(field_office__field_office_number__icontains=freetext) |
                    Q(system_unit_type__unit_type__icontains=freetext) |
                    Q(field_office__field_office_name__icontains=freetext))
        return queryset


class SystemUnitTypeViewSet(HistoryViewSet):
    queryset = SystemUnitType.objects.all()
    serializer_class = SystemUnitTypeSerializer
    permission_classes = (permissions.IsAuthenticated,)


class SystemUnitProhibitionDateViewSet(HistoryViewSet):
    serializer_class = SystemUnitProhibitionDateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    # override the default queryset to allow filtering by URL arguments
    def get_queryset(self):
        queryset = SystemUnitProhibitionDate.objects.all()
        if self.request:
            # filter by unit ID, exact
            unit_id = self.request.query_params.get('unit', None)
            if unit_id is not None:
                queryset = queryset.filter(system_unit_id__exact=unit_id)
            # filter by freetext, case-insensitive contain
            freetext = self.request.query_params.get('freetext', None)
            if freetext is not None:  # trying to compare freetext to a formatted prohibition date, not working
                if '/' in freetext:
                    # only perform date comparisons if all date parts are integers
                    isinteger = True
                    date_parts = freetext.strip('/').split('/')
                    for date_part in date_parts:
                        if not date_part.isnumeric() or not float(date_part).is_integer():
                            isinteger = False
                    if isinteger:
                        counter = len(date_parts)
                        # month
                        if counter == 1:
                            month_places = len(date_parts[0])
                            if month_places <= 2:
                                queryset = queryset.filter(prohibition_date__month=int(date_parts[0]))
                            else:
                                queryset = SystemUnitProhibitionDate.objects.none()
                        # day
                        elif counter == 2:
                            day_places = len(date_parts[1])
                            if day_places <= 2:
                                queryset = queryset.filter(
                                    prohibition_date__month=int(date_parts[0]),
                                    prohibition_date__day=int(date_parts[1]))
                            else:
                                queryset = SystemUnitProhibitionDate.objects.none()
                        # year
                        elif counter == 3:
                            year_places = len(date_parts[2])
                            year_int = int(date_parts[2])
                            year_part = None
                            if year_places == 1:
                                year_part = 2000 + year_int
                            elif year_places == 2:
                                year_part = 1900 + year_int if 99 >= year_int >= 83 else 2000 + year_int
                            elif year_places == 4:
                                year_part = year_int
                            if year_part:
                                # cannot filter on a three digit year
                                queryset = queryset.filter(
                                    prohibition_date__month=int(date_parts[0]),
                                    prohibition_date__day=int(date_parts[1]),
                                    prohibition_date__year=year_part)
                            else:
                                queryset = SystemUnitProhibitionDate.objects.none()
                        else:
                            queryset = SystemUnitProhibitionDate.objects.none()
                    else:
                        queryset = SystemUnitProhibitionDate.objects.none()
                else:
                    queryset = queryset.filter(system_unit__system_unit_number__icontains=freetext)
        return queryset


class SystemUnitMapViewSet(HistoryViewSet):
    serializer_class = SystemUnitMapSerializer
    permission_classes = (permissions.IsAuthenticated,)

    # override the default queryset to allow filtering by URL arguments
    def get_queryset(self):
        queryset = SystemUnitMap.objects.all()
        if self.request:
            # filter by unit ID, exact
            unit_id = self.request.query_params.get('unit', None)
            if unit_id is not None:
                queryset = queryset.filter(system_unit__exact=unit_id)
            # filter by map ID, exact
            map_id = self.request.query_params.get('map', None)
            if map_id is not None:
                queryset = queryset.filter(system_map__exact=map_id)
        return queryset


class SystemMapViewSet(HistoryViewSet):
    serializer_class = SystemMapSerializer
    permission_classes = (permissions.IsAuthenticated,)

    # override the default queryset to allow filtering by URL arguments
    def get_queryset(self):
        # prefetch_related only the exact, necessary fields to greatly improve the response time of the query
        queryset = SystemMap.objects.all()#.prefetch_related(
            #Prefetch('system_units', queryset=SystemUnit.objects.only('system_unit_number').all())).all()
        if self.request:
            # filter by unit ID, exact
            unit_id = self.request.query_params.get('unit', None)
            if unit_id is not None:
                queryset = queryset.filter(system_units__exact=unit_id)
            # filter by freetext, case-insensitive contain
            freetext = self.request.query_params.get('freetext', None)
            if freetext is not None:
                queryset = queryset.filter(
                    Q(system_units__system_unit_number__icontains=freetext) |
                    Q(map_number__icontains=freetext) |
                    Q(map_title__icontains=freetext) |
                    Q(effective__icontains=freetext) |
                    Q(map_date__icontains=freetext))
        return queryset


class FieldOfficeViewSet(HistoryViewSet):
    queryset = FieldOffice.objects.all()
    serializer_class = FieldOfficeSerializer
    permission_classes = (permissions.IsAuthenticated,)


######
#
# Reports
#
######


class ReportCaseView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = StandardResultsSetPagination
    filename = ""

    # override the default renderers to use a custom csv renderer when requested
    # note that these custom renderers have hard-coded field name headers that match the their respective serialzers
    # from when this code was originally written, so if the serializer fields change, these renderer field name headers
    # won't match the serializer data, until the renderer code is manually updated to match the serializer fields
    def get_renderers(self):
        default_renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
        if self.request:
            frmt = self.request.query_params.get('format', None)
            report = self.request.query_params.get('report', None)
            if frmt is not None and frmt == 'csv':
                if report is not None and report == 'casesbyunit':
                    renderer_classes = (ReportCasesByUnitCSVRenderer,) + tuple(default_renderer_classes)
                elif report is not None and report == 'daystoresolution':
                    renderer_classes = (ReportDaysToResolutionCSVRenderer,) + tuple(default_renderer_classes)
                elif report is not None and report == 'daystoeachstatus':
                    renderer_classes = (ReportDaysToEachStatusCSVRenderer,) + tuple(default_renderer_classes)
                elif report is not None and report == 'allcasesforuser':
                    renderer_classes = (ReportCasesForUserCSVRenderer,) + tuple(default_renderer_classes)
                else:
                    renderer_classes = (PaginatedCSVRenderer,) + tuple(default_renderer_classes)
            else:
                renderer_classes = tuple(default_renderer_classes)
        else:
            renderer_classes = tuple(default_renderer_classes)
        return [renderer_class() for renderer_class in renderer_classes]

    # override the default serializer_class if format is specified
    def get_serializer_class(self):
        if self.request:
            report = self.request.query_params.get('report', None)
            cbrs_unit = self.request.query_params.get('cbrs_unit', None)
            user = self.request.query_params.get('user', None)
            # if report is not specified or not equal to an approved report, assume generic report
            if report is not None and report == 'casesbyunit':
                self.filename = "Report_CasesByUnit_"
                if cbrs_unit is not None:
                    self.filename += cbrs_unit + "_"
                return ReportCasesByUnitSerializer
            elif report is not None and report == 'daystoresolution':
                self.filename = "Report_DaysToResolution_"
                return ReportDaysToResolutionSerializer
            elif report is not None and report == 'daystoeachstatus':
                self.filename = "Report_DaysToEachStatus_"
                return ReportDaysToEachStatusSerializer
            elif report is not None and report == 'allcasesforuser':
                self.filename = "Report_CasesForUser_"
                if user is not None:
                    self.filename += user + "_"
                return ReportCasesForUserSerializer
            else:
                return ReportSerializer
        else:
            return ReportSerializer

    # override the default finalize_response to assign a filename to CSV files
    # see https://github.com/mjumbewu/django-rest-framework-csv/issues/15
    def finalize_response(self, request, response, *args, **kwargs):
        response = super(generics.ListAPIView, self).finalize_response(request, response, *args, **kwargs)
        # join list of tag numbers
        for item in response.data.get('results'):
            for key, value in item.items():
                if isinstance(item[key], list):  # can do this better
                    item[key] = ','.join(str(v) for v in value)
        if request and request.accepted_renderer.format == 'csv':
            self.filename += dt.now().strftime("%Y") + '-' + dt.now().strftime("%m") + '-' + dt.now().strftime(
                "%d") + '.csv'
            response['Content-Disposition'] = "attachment; filename=%s" % self.filename
            response['Access-Control-Expose-Headers'] = 'Content-Disposition'
        return response

    # override the default queryset to allow filtering by URL arguments
    def get_queryset(self):
        queryset = ReportCase.objects.all().order_by('id')
        if self.request:
            # filter by CBRS unit IDs, exact list
            cbrs_unit = self.request.query_params.get('cbrs_unit', None)
            if cbrs_unit is not None:
                cbrs_unit_list = cbrs_unit.split(',')
                queryset = queryset.filter(cbrs_unit__in=cbrs_unit_list).order_by('id')
            # filter by user
            user = self.request.query_params.get('user', None)
            if user is not None:
                queryset = queryset.filter(
                    Q(analyst__username__iexact=user) |
                    Q(qc_reviewer__username__iexact=user))
                    # Q(comments__comment__icontains=user)) # some comments mention users, but not able to get this returned
            # filter by range for date field (after only, before only, or between, depending on which URL params appear)
            report = self.request.query_params.get('report', None)
            if report is not None and report == 'daystoeachstatus':
                date_field = self.request.query_params.get('date_field', None)
                if date_field is not None:
                    from_date = self.request.query_params.get('from_date', None)
                    to_date = self.request.query_params.get('to_date', None)
                    if from_date is not None and to_date is not None:
                        # the filter below using __range is date-inclusive
                        # queryset = queryset.filter(report__some_date__range=(from_date, to_date))
                        # the filter below is date-exclusive
                        filtergt = date_field + '__gt'
                        filterlt = date_field + '__lt'
                        kw_args = {filtergt: from_date, filterlt: to_date}
                        queryset = queryset.filter(**kw_args)
                    elif from_date is not None:
                        filtergt = date_field + '__gt'
                        queryset = queryset.filter(**{filtergt: from_date})
                    elif to_date is not None:
                        filterlt = date_field + '__lt'
                        queryset = queryset.filter(**{filterlt: to_date})
        return queryset


class ReportCaseCountView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ReportCountOfCasesByStatusSerializer
    filename = "Report_CountCasesByStatus_"

    # override the default renderers to use a custom csv renderer when requested
    # note that these custom renderers have hard-coded field name headers that match the their respective serialzers
    # from when this code was originally written, so if the serializer fields change, these renderer field name headers
    # won't match the serializer data, until the renderer code is manually updated to match the serializer fields
    def get_renderers(self):
        frmt = self.request.query_params.get('format', None) if self.request else None
        if frmt is not None and frmt == 'csv':
            renderer_classes = (ReportCaseCountCSVRenderer,) + tuple(api_settings.DEFAULT_RENDERER_CLASSES)
        else:
            renderer_classes = tuple(api_settings.DEFAULT_RENDERER_CLASSES)
        return [renderer_class() for renderer_class in renderer_classes]

    # override the default finalize_response to assign a filename to CSV files
    # see https://github.com/mjumbewu/django-rest-framework-csv/issues/15
    def finalize_response(self, request, response, *args, **kwargs):
        response = super(ReportCaseCountView, self).finalize_response(request, response, *args, **kwargs)
        if request and request.accepted_renderer.format == 'csv':
            self.filename += dt.now().strftime("%Y") + '-' + dt.now().strftime("%m") + '-' + dt.now().strftime(
                "%d") + '.csv'
            response['Content-Disposition'] = "attachment; filename=%s" % self.filename
            response['Access-Control-Expose-Headers'] = 'Content-Disposition'
        return response

    def get(self, request):
        data = [ReportCase.report_case_counts.count_cases_by_status()]
        return Response(data)


######
#
#  Users
#
######


class UserViewSet(HistoryViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request:
            user = self.request.user
        else:
            user = None
        if not user or not user.is_active:
            queryset = User.objects.none()
        else:
            # do not return the admin and public users
            queryset = User.objects.all().exclude(id__in=[1, 2])
            if self.request:
                # filter by username, exact
                username = self.request.query_params.get('username', None)
                if username is not None:
                    queryset = queryset.filter(username__exact=username)
                # filter by is_active, exact
                is_active = self.request.query_params.get('is_active', None)
                if is_active is not None:
                    queryset = queryset.filter(is_active__exact=is_active)
                # filter by current and former active users
                used_users = self.request.query_params.get('used_users', None)
                if used_users is not None:
                    active_users = queryset.filter(is_active__exact=True)
                    analysts = queryset.filter(analyst__isnull=False).distinct()
                    qc_reviewers = queryset.filter(qc_reviewer__isnull=False).distinct()
                    fws_reviewers = queryset.filter(fws_reviewer__isnull=False).distinct()
                    used_users_chain = list(chain(active_users, analysts, qc_reviewers, fws_reviewers))
                    used_users_set = set(used_users_chain)
                    used_users_ids = []
                    for used_user in used_users_set:
                        used_users_ids.append(used_user.id)
                    queryset = queryset.filter(id__in=used_users_ids).extra(order_by=['-is_active', 'username'])
                # filter by freetext, case-insensitive contain
                freetext = self.request.query_params.get('freetext', None)
                if freetext is not None:
                    queryset = queryset.filter(
                        Q(first_name__icontains=freetext) |
                        Q(last_name__icontains=freetext) |
                        Q(email__icontains=freetext) |
                        Q(is_active__icontains=freetext) |
                        Q(is_superuser__icontains=freetext) |
                        Q(is_staff__icontains=freetext) |
                        Q(username__icontains=freetext))
        return queryset


class AuthView(views.APIView):
    authentication_classes = (authentication.BasicAuthentication,)
    serializer_class = UserSerializer

    def post(self, request):
        return Response(self.serializer_class(request.user).data)
