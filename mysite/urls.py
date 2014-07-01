from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from django.contrib.auth.views import login
import paw.urls

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += patterns('',
    url(r'', include('paw.urls')),
)
