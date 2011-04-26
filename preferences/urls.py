from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('preferences.views',
    (r'^$', 'index'),
    (r'^media/(.*)$','media'),
    url(r'^change/(?P<app>[a-z_\-]*)/(?P<pref>[a-z_\-]*)/(?P<new_value>.*)/$','change'),
)
