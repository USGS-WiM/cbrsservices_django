from django.conf.urls import patterns, url, include
from cbraservices import views, receivers
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register(r'cases', views.CaseViewSet, 'cases')
router.register(r'casefiles', views.CaseFileViewSet, 'casefiles')
router.register(r'properties', views.PropertyViewSet, 'properties')
router.register(r'requesters', views.RequesterViewSet, 'requesters')
router.register(r'casetags', views.CaseTagViewSet, 'casetags')
router.register(r'tags', views.TagViewSet, 'tags')
router.register(r'comments', views.CommentViewSet, 'comments')
router.register(r'determinations', views.DeterminationViewSet, 'determinations')
router.register(r'systemunits', views.SystemUnitViewSet, 'systemunits')
router.register(r'systemunitprohibitiondates', views.SystemUnitProhibitionDateViewSet, 'systemunitprohibitiondates')
router.register(r'systemunitmaps', views.SystemUnitMapViewSet, 'systemunitmaps')
router.register(r'systemmaps', views.SystemMapViewSet, 'systemmaps')
router.register(r'fieldoffices', views.FieldOfficeViewSet, 'fieldoffices')
router.register(r'users', views.UserViewSet, 'users')

urlpatterns = patterns('',
                       url(r'^', include(router.urls)),
                       url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                       url(r'^auth/$', views.AuthView.as_view(), name='authenticate'),
                       url(r'^reportcases/$', views.ReportCaseView.as_view(), name='reportcases'),
                       url(r'^reportcasecounts/$', views.ReportCaseCountView.as_view(), name='reportcasecounts')
                       )
