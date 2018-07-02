from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view
from . import views

schema_view = get_swagger_view(title='TOMIS NptAdwords API')

urlpatterns = [
    url(
        r'^api/v1/records/(?P<pk>[0-9]+)$',
        views.get_delete_update_record,
        name='get_delete_update_record'
    ),
    url(
        r'^api/v1/records/$',
        views.get_post_records,
        name='get_post_records'
    ),
    url(
        r'^$', schema_view
    )
]
