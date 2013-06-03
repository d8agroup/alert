from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^%s/' % settings.ODC_URL, include('django_odc.urls')),
    url(r'^%s/' % settings.ADMIN_URL, include(admin.site.urls)),
)
