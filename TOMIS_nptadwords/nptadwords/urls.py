from django.conf.urls import url
from django.urls import include, path
from rest_framework_swagger.views import get_swagger_view
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

schema_view = get_swagger_view(title='TOMIS NptAdwords API')

urlpatterns = [
    url(
        r'^api/v1/records/(?P<pk>[0-9]+)$',
        views.RecordDetail.as_view()
    ),
    url(
        r'^api/v1/records/$',
        views.RecordList.as_view()
    ),
    url(
        r'^swagger/$', schema_view
    ),
    path('api/v1/rest-auth/', include('rest_auth.urls')),
    url(r'^$', views.homepage, name='homepage'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
