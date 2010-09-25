from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import direct_to_template

from paulo.sweetness import View
from sampleapp import views

urlpatterns = patterns(
    '',
    url(r'^$', direct_to_template, {'template':'sampleapp/index.html'}),

    url(r'^one/$', View(views.SampleOne)),
    url(r'^one/(.*)/$', View(views.SampleOneWithParams)),

    url(r'^two/$', views.SampleTwo.view),

    url(r'^three/$', views.SampleThree.view),

    url(r'^four/$', views.SampleFour.view),

    url(r'^five/(.*)/(.*)/$', views.SampleFive.view),

    url(r'^six/(?P<kwarg>.*)/(?P<blarg>.*)/$', views.SampleSix.view),
    url(r'^six/(?P<kwarg>.*)/$', views.SampleSix.view),

    url(r'^seven/(?P<slug>[\w-]*)/and/(?P<other_slug>[\w-]*)/$', views.SampleSeven.view),
    url(r'^seven/(?P<slug>[\w-]*)/and/(?P<other_slug>[\w-]*)/with/(?P<username>.*)/$', views.SampleSeven.view),

)
