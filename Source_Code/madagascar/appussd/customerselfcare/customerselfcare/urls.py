from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from myadmin.admin import CusPassChangeForm
from customerservice.views import CusPasswordChangeForm

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', 'customerselfcare.views.home', name='home'),
                       url(r'^whitelist/', include('whitelist.urls')),
                       url(r'^accounts/login/', 'customerselfcare.views.home'),
                       url(r'^3g/$', 'customerservice.views.threeg'),
                       url(r'^provision/$', 'customerservice.views.provision'),
                       url(r'^audittrail/$', 'audittrail.views.audit_trail'),
                       url(r'^json/packages/', 'packages.views.packagesJson'),
                       url(r'^xml/packages/', 'packages.views.packagesXml'),
                       url(r'^logout/$', 'customerselfcare.views.log_out'),
                       url(r'^me2u/$', 'me2u.views.me2u'),
                       url(r'^me2u/export/(?P<msisdn>\d+)/$',
                           'me2u.views.export_me2u'),
                       url(r'^admin/password_change/$', RedirectView.as_view(
                           url='/accounts/change_password/')),
                       url(r'^accounts/change_password/$',
                           'django.contrib.auth.views.password_change',
                           {'password_change_form': CusPasswordChangeForm,
                            'post_change_redirect': '/accounts/change_password/done/'},
                           name='password_change'),
                       url(r'^accounts/change_password/done/$',
                           'django.contrib.auth.views.password_change_done'),
                       url(r'^(\d+)/password/$',
                           'django.contrib.auth.views.password_change',
                           {'password_change_form': CusPassChangeForm}),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^history/(?P<msisdn>\d+)/$',
                           'customerservice.views.history3g'),
                       url(r'^renewhistory/(?P<msisdn>\d+)/$',
                           'customerservice.views.historyrenew'),
                       url(r'^export_history/(?P<msisdn>\d+)/$',
                           'customerservice.views.history3g'),
                       url(r'^export_rhistory/(?P<msisdn>\d+)/$',
                           'customerservice.views.history3g'),
                       url(r'^export_audit/', 'audittrail.views.export_audit'),
                       )
