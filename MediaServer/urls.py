from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from MS.views import remove_file, file_upload, index

urlpatterns = patterns('',
                       url(r'^$', index),
                       url(r'^remove_file/$', remove_file),
                       url(r'^file_upload/$', file_upload)
)
