import json
from django.contrib.auth import authenticate, login, logout
from rest_framework import views, viewsets, permissions, authentication, status
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from rest_framework_extensions.cache.mixins import ListCacheResponseMixin
from cbraservices.serializers import *
from cbraservices.models import *


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
#  Determinations
#
######


class CaseViewSet(viewsets.ModelViewSet):
    queryset = Case.objects.all()
    # serializer_class = CaseSerializer
    # permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        view = self.request.query_params.get('view', None)
        # if view is not specified or not equal to workbench, assume case
        if view is not None and view == 'workbench':
            return WorkbenchSerializer
        else:
            return CaseSerializer


class CaseFileViewSet(viewsets.ModelViewSet):
    # queryset = CaseFile.objects.all()
    serializer_class = CaseFileSerializer
    # permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser,)

    def perform_create(self, serializer):
        print(self.request.user)

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


class PropertyViewSet(viewsets.ModelViewSet):
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
        return queryset


class RequesterViewSet(viewsets.ModelViewSet):
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
        return queryset


######
#
#  Tags
#
######


class CaseTagViewSet(viewsets.ModelViewSet):
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


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    # permission_classes = (permissions.IsAuthenticated,)


######
#
#  Comments
#
######


class CommentViewSet(viewsets.ModelViewSet):
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


class DeterminationViewSet(viewsets.ModelViewSet):
    queryset = Determination.objects.all()
    serializer_class = DeterminationSerializer
    # permission_classes = (permissions.IsAuthenticated,)


class SystemUnitViewSet(CacheResponseMixin, viewsets.ModelViewSet):
    queryset = SystemUnit.objects.all()
    serializer_class = SystemUnitSerializer
    # permission_classes = (permissions.IsAuthenticated,)


class SystemUnitProhibitionDateViewSet(viewsets.ModelViewSet):
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


class SystemUnitMapViewSet(viewsets.ModelViewSet):
    queryset = SystemUnitMap.objects.all()
    serializer_class = SystemUnitMapSerializer
    # permission_classes = (permissions.IsAuthenticated,)


class SystemMapViewSet(viewsets.ModelViewSet):
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


class FieldOfficeViewSet(viewsets.ModelViewSet):
    queryset = FieldOffice.objects.all()
    serializer_class = FieldOfficeSerializer
    # permission_classes = (permissions.IsAuthenticated,)


######
#
#  Users
#
######


class UserViewSet(viewsets.ModelViewSet):
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
