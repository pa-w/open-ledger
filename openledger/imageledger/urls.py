from django.conf.urls import url, include

from rest_framework.urlpatterns import format_suffix_patterns
from django_cas_ng.views import login as cas_login, logout as cas_logout, callback as cas_callback

from imageledger.views import search_views, api_views

urlpatterns = [
    url(r'^$', search_views.index, name='index'),
    url(r'^provider-apis$', search_views.provider_apis, name='provider-apis'),
    url(r'^provider/(?P<provider>\w+)$', search_views.by_provider, name='by-provider'),
    url(r'^image/detail$', search_views.by_image, name="by-image"),
    url(r'^image/detail/(?P<identifier>.*)$', search_views.detail, name="detail"),

    # CAS
    url(r'^accounts/login$', cas_login, name='cas_ng_login'),
    url(r'^accounts/logout$', cas_logout, name='cas_ng_logout'),
    url(r'^accounts/callback$', cas_callback, name='cas_ng_proxy_callback'),

]

apipatterns = [
    url(r'^api/v1/lists$', api_views.ListList.as_view()),
]

apipatterns = format_suffix_patterns(apipatterns)

urlpatterns += apipatterns
