from django.conf.urls import patterns, url

urlpatterns = patterns('whitelist.views',
                       url(r'^$', 'whitelist'),
                       url(r'^do/$', 'process_list'),
                       url(r'^bulk/$', 'process_bulk'),
                       url(r'^export/(?P<report>\d+)/$', 'export_report'),
                       )
