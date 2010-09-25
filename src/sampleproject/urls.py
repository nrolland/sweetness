from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns(
    '',
    url(r'^sample/', include('sampleapp.urls')),
    url(r'^$', direct_to_template, {'template':"index.html"}),
)
