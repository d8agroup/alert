from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

import views

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^signin$', views.signin, name='signin'),
    url(r'^signout$', views.signout, name='signout'),

    url(r'^$', views.home, name='home'),

    url(r'^admin/users_summary$', views.admin_users_summary, name='admin_users_summary'),

    url(r'^curate/(?P<dataset_id>\w+)$', views.curate_dataset, name='curate'),

    url(r'^%s/' % settings.ODC_URL, include('django_odc.urls')),
    url(r'^%s/' % settings.ADMIN_URL, include(admin.site.urls)),
)
