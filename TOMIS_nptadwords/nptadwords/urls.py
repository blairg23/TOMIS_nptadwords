from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        r'^api/v1/record/(?P<pk>[0-9]+)$',
        views.get_delete_update_record,
        name='get_delete_update_record'
    ),
    url(
        r'^api/v1/records/$',
        views.get_post_records,
        name='get_post_records'
    )
]
