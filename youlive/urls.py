from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from django.contrib.auth.views import login
#from django.views.static import serve as statv
import django.views.static
import paw.views

urlpatterns = patterns('',
    url(r'^$', paw.views.index),
    url(r'^hello/', paw.views.hello),
    url(r'^login/', paw.views.login),
    url(r'^logout/', paw.views.logout),
    url(r'^f5handle/', paw.views.putfilenames),
)
