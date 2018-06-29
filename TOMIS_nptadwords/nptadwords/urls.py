from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        r'^api/v1/accounts/(?P<pk>[0-9]+)$',
        views.get_delete_update_account,
        name='get_delete_update_account'
    ),
    url(
        r'^api/v1/accounts/$',
        views.get_post_accounts,
        name='get_post_accounts'
    )
]
