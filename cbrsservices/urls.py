from django.urls import path
from django.conf.urls import url, include
from django.views.generic.base import TemplateView
from cbrsservices import views
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view


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
router.register(r'systemunittypes', views.SystemUnitTypeViewSet, 'systemunittypes')
router.register(r'systemunitprohibitiondates', views.SystemUnitProhibitionDateViewSet, 'systemunitprohibitiondates')
router.register(r'systemunitmaps', views.SystemUnitMapViewSet, 'systemunitmaps')
router.register(r'systemmaps', views.SystemMapViewSet, 'systemmaps')
router.register(r'fieldoffices', views.FieldOfficeViewSet, 'fieldoffices')
router.register(r'users', views.UserViewSet, 'users')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('openapi', get_schema_view(title="CBRSServices", description="API for CBRS DMS"), name='openapi-schema'),
    path('swagger-ui/', TemplateView.as_view(template_name='swagger-ui.html',
                                             extra_context={'schema_url': 'openapi-schema'}), name='swagger-ui'),
    path('redoc/', TemplateView.as_view(template_name='redoc.html',
                                        extra_context={'schema_url': 'openapi-schema'}), name='redoc'),
    url(r'^auth/$', views.AuthView.as_view(), name='authenticate'),
    url(r'^reportcases/$', views.ReportCaseView.as_view(), name='reportcases'),
    url(r'^reportcasecounts/$', views.ReportCaseCountView.as_view(), name='reportcasecounts')
]
