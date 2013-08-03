from django.conf.urls import patterns, include, url
from api.views import PackagesListView, PackagesFindView


urlpatterns = patterns('',
    url(r'^packages/$', PackagesListView.as_view(), name='list'),
    url(r'^packages/(?P<name>\w+)/$', PackagesFindView.as_view(), name='find')
)
