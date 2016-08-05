import json
from datetime import datetime as dt
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.db.models.expressions import RawSQL
from rest_framework import views, viewsets, permissions, authentication, status
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from rest_framework_extensions.cache.mixins import ListCacheResponseMixin
from cbraservices.serializers import *
from cbraservices.models import *
from cbraservices.permissions import *
from cbraservices.renderers import *


########################################################################################################################
#
#  copyright: 2016 WiM - USGS
#  authors: Aaron Stephenson USGS WiM (Wisconsin Internet Mapping)
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
        serializer.save(created_by=self.request.user)
        serializer.save(modified_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user)


######
#
#  Determinations
#
######


class CaseViewSet(HistoryViewSet):
    # queryset = Case.objects.all()
    # serializer_class = CaseSerializer
    # permission_classes = (permissions.IsAuthenticated,)

    # override the default renderers to use a custom DOCX renderer when requested
    def get_renderers(self):
        frmt = self.request.query_params.get('format', None)
        if frmt is not None and frmt == 'docx':
            renderer_classes = (FinalLetterDOCXRenderer,) + tuple(api_settings.DEFAULT_RENDERER_CLASSES)
        else:
            renderer_classes = tuple(api_settings.DEFAULT_RENDERER_CLASSES)
        return [renderer_class() for renderer_class in renderer_classes]

    # override the default serializer_class if workbench or report format is specified
    def get_serializer_class(self):
        view = self.request.query_params.get('view', None)
        # if view is not specified or not equal to workbench or report, assume case
        if view is not None and view == 'workbench':
            return WorkbenchSerializer
        elif view is not None and view == 'report':
            return ReportSerializer
        elif self.request.accepted_renderer.format == 'docx':
            return LetterSerializer
        else:
            return CaseSerializer

    # override the default finalize_response to assign a filename to DOCX files
    # see https://github.com/mjumbewu/django-rest-framework-csv/issues/15
    def finalize_response(self, request, *args, **kwargs):
        response = super(viewsets.ModelViewSet, self).finalize_response(request, *args, **kwargs)
        if self.request.accepted_renderer.format == 'docx':
            filename = 'final_letter_case_'
            filename += self.get_queryset().first().case_hash + '_'
            filename += dt.now().strftime("%Y") + '-' + dt.now().strftime("%m") + '-' + dt.now().strftime("%d")
            filename += '.docx'
            response['Content-Disposition'] = "attachment; filename=%s" % filename
            response['Access-Control-Expose-Headers'] = 'Content-Disposition'
        return response

    # override the default queryset to allow filtering by URL arguments
    def get_queryset(self):
        queryset = Case.objects.all()
        # filter by case hash, exact
        case_hash = self.request.query_params.get('case_hash', None)
        if case_hash is not None:
            queryset = queryset.filter(case_hash__exact=case_hash)
        # filter by property ID, exact
        property = self.request.query_params.get('property', None)
        if property is not None:
            queryset = queryset.filter(property__exact=property)
        # filter by requester ID, exact
        requester = self.request.query_params.get('requester', None)
        if requester is not None:
            queryset = queryset.filter(requester__exact=requester)
        # filter by status, exact list
        status = self.request.query_params.get('status', None)
        if status is not None:
            status_list = status.split(',')
            queryset = queryset.filter(status__in=status_list)
        # filter by case number, exact list
        case_number = self.request.query_params.get('case_number', None)
        if case_number is not None:
            #print(str(case_number))
            case_number_list = case_number.split(',')
            queryset = queryset.filter(id__in=case_number_list)
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
        # filter by tag IDs, exact list
        tags = self.request.query_params.get('tags', None)
        if tags is not None:
            tag_list = tags.split(',')
            queryset = queryset.filter(tags__in=tag_list)
        # filter by priority, exact
        priority = self.request.query_params.get('priority', None)
        if priority is not None:
            queryset = queryset.filter(priority__exact=priority)
        # # filter by on_hold, exact
        # on_hold = self.request.query_params.get('on_hold', None)
        # if on_hold is not None:
        #     queryset = queryset.filter(on_hold__exact=on_hold)
        # # filter by invalid, exact
        # invalid = self.request.query_params.get('invalid', None)
        # if invalid is not None:
        #     queryset = queryset.filter(invalid__exact=invalid)
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
                #Q(case_number__icontains=freetext) |
                #Q(RawSQL("SELECT id FROM cbra_case WHERE id::varchar ILIKE %s", freetext)) | #("'%'" + freetext + "'%'",))) |
                Q(cbrs_unit__system_unit_name__icontains=freetext) |
                Q(property__street__icontains=freetext) |
                Q(property__unit__icontains=freetext) |
                Q(property__city__icontains=freetext))
        return queryset


class CaseFileViewSet(HistoryViewSet):
    # queryset = CaseFile.objects.all()
    serializer_class = CaseFileSerializer
    # permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser,)

    # override the default create to include user information
    def perform_create(self, serializer):
        # print(self.request.user)

        def get_user():
            if self.request.user.is_anonymous():
                return None
            else:
                return self.request.user

        serializer.save(case=Case.objects.get(pk=int(self.request.data.get('case'))),
                        file=self.request.data.get('file'),
                        uploader=get_user())

    # override the default queryset to allow filtering by URL arguments
    def get_queryset(self):
        queryset = CaseFile.objects.all()
        # filter by case ID, exact
        case_id = self.request.query_params.get('case', None)
        if case_id is not None:
            queryset = queryset.filter(case__exact=case_id)
        return queryset


class PropertyViewSet(HistoryViewSet):
    # queryset = Property.objects.all()
    serializer_class = PropertySerializer
    # permission_classes = (permissions.IsAuthenticated,)

    # override the default queryset to allow filtering by URL arguments
    def get_queryset(self):
        queryset = Property.objects.all()
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
        return queryset


class RequesterViewSet(HistoryViewSet):
    # queryset = Requester.objects.all()
    serializer_class = RequesterSerializer
    # permission_classes = (permissions.IsAuthenticated,)

    # override the default queryset to allow filtering by URL arguments
    def get_queryset(self):
        queryset = Requester.objects.all()
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
    # queryset = CaseTag.objects.all()
    serializer_class = CaseTagSerializer
    # permission_classes = (permissions.IsAuthenticated,)

    # override the default queryset to allow filtering by URL arguments
    def get_queryset(self):
        queryset = CaseTag.objects.all()
        # filter by case ID, exact
        case_id = self.request.query_params.get('case', None)
        if case_id is not None:
            queryset = queryset.filter(case_id__exact=case_id)
        return queryset


class TagViewSet(HistoryViewSet):
    # queryset = Tag.objects.all()
    serializer_class = TagSerializer
    # permission_classes = (permissions.IsAuthenticated,)

    # override the default queryset to allow filtering by URL arguments
    def get_queryset(self):
        queryset = Tag.objects.all()
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
    # queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # permission_classes = (permissions.IsAuthenticated,)

    # override the default queryset to allow filtering by URL arguments
    def get_queryset(self):
        queryset = Comment.objects.all()
        # filter by case ID, exact
        case_id = self.request.query_params.get('case', None)
        if case_id is not None:
            queryset = queryset.filter(case_id__exact=case_id)
        return queryset


######
#
#  Lookup Tables
#
######


class DeterminationViewSet(HistoryViewSet):
    queryset = Determination.objects.all()
    serializer_class = DeterminationSerializer
    # permission_classes = (permissions.IsAuthenticated,)


class SystemUnitViewSet(CacheResponseMixin, HistoryViewSet):
    queryset = SystemUnit.objects.all()
    serializer_class = SystemUnitSerializer
    # permission_classes = (permissions.IsAuthenticated,)


class SystemUnitProhibitionDateViewSet(HistoryViewSet):
    # queryset = SystemUnitProhibitionDate.objects.all()
    serializer_class = SystemUnitProhibitionDateSerializer
    # permission_classes = (permissions.IsAuthenticated,)

    # override the default queryset to allow filtering by URL arguments
    def get_queryset(self):
        queryset = SystemUnitProhibitionDate.objects.all()
        # filter by case ID, exact
        unit_id = self.request.query_params.get('unit', None)
        if unit_id is not None:
            queryset = queryset.filter(system_unit_id__exact=unit_id)
        return queryset


class SystemUnitMapViewSet(HistoryViewSet):
    queryset = SystemUnitMap.objects.all()
    serializer_class = SystemUnitMapSerializer
    # permission_classes = (permissions.IsAuthenticated,)


class SystemMapViewSet(HistoryViewSet):
    # queryset = SystemMap.objects.all()
    serializer_class = SystemMapSerializer
    # permission_classes = (permissions.IsAuthenticated,)

    # override the default queryset to allow filtering by URL arguments
    def get_queryset(self):
        queryset = SystemMap.objects.all()
        # filter by case ID, exact
        unit_id = self.request.query_params.get('unit', None)
        if unit_id is not None:
            queryset = queryset.filter(system_units__exact=unit_id)
        return queryset


class FieldOfficeViewSet(HistoryViewSet):
    queryset = FieldOffice.objects.all()
    serializer_class = FieldOfficeSerializer
    # permission_classes = (permissions.IsAuthenticated,)


######
#
#  Users
#
######


class UserViewSet(HistoryViewSet):
    # permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def get_queryset(self):
        # do not return the admin and public users
        queryset = User.objects.all().exclude(id__in=[1, 2])
        # filter by username, exact
        username = self.request.query_params.get('username', None)
        if username is not None:
            queryset = queryset.filter(username__exact=username)
        return queryset


class AuthView(views.APIView):
    authentication_classes = (authentication.BasicAuthentication,)
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        return Response(self.serializer_class(request.user).data)


# class UserLoginView(views.APIView):
#     def post(self, request):
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(username=username, password=password)
#
#         if user is not None:
#             if user.is_active:
#                 login(request, user)
#                 #logger.info("Logged In")
#                 data = UserSerializer(user).data
#                 return Response(data, status=status.HTTP_200_OK)
#             else:
#                 #logger.info("Account is disabled: {0}".format(username))
#                 data = json.dumps({"status": "Unauthorized", "message": "Your account is disabled."})
#                 return Response(data, status=status.HTTP_401_UNAUTHORIZED)
#
#         else:
#             #logger.info("Invalid login details: {0}, {1}".format(username, password))
#             data = json.dumps({"status": "Unauthorized", "message": "Invalid login details supplied."})
#             return Response(data, status=status.HTTP_401_UNAUTHORIZED)
#
#
# class UserLogoutView(views.APIView):
#     permission_classes = (permissions.IsAuthenticated,)
#
#     def post(self, request):
#         logout(request)
#         #logger.info("Logged Out")
#
#         return Response({}, status=status.HTTP_204_NO_CONTENT)
