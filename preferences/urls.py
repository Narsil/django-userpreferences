from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('preferences.views',
    (r'^$', 'index'),
    (r'^media/(.*)$','media'),
)
