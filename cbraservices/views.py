import json
from django.contrib.auth import authenticate, login, logout
from rest_framework import views, viewsets, permissions, authentication, status
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from rest_framework_extensions.cache.mixins import ListCacheResponseMixin
from cbraservices.serializers import *
from cbraservices.models import *
from cbraservices.permissions import *


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

    def get_serializer_class(self):
        view = self.request.query_params.get('view', None)
        # if view is not specified or not equal to workbench, assume case
        if view is not None and view == 'workbench':
            return WorkbenchSerializer
        else:
            return CaseSerializer

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
        return queryset


class CaseFileViewSet(HistoryViewSet):
    # queryset = CaseFile.objects.all()
    serializer_class = CaseFileSerializer
    # permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser,)

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
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    # permission_classes = (permissions.IsAuthenticated,)


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
