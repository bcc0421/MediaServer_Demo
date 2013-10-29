from django.conf.urls import patterns, include, url

from MS.views import remove_file, file_upload, index, attachment

urlpatterns = patterns('',
                       url(r'^$', index),
                       url(r'^remove_file/$', remove_file),
                       url(r'^file_upload/$', file_upload),
                       url(r'^attachment/(?P<file_name>.+)/$', attachment),
                       url(r'^thumbnail/(?P<name>.+)/$', thumbnail),
                       url(r'^play/(?P<file_name>.+)/$', index),
)
