from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('social_auth.urls')),

    url(r'^$', 'campmanager.views.index'),
    url(r'^burners/$', 'campmanager.views.burnerlist'),
    url(r'^bigstuff/$', 'campmanager.views.bigstufflist'),

    url(r'^subcamp/(?P<subcamp>[^/]+)/$', 'campmanager.views.subcamp'),
    url(r'^group/(?P<siteid>[^/]+)/$', 'campmanager.group.group'),
    url(r'^group/(?P<siteid>[^/]+)/bigstuff/(?P<stuffid>\d+)/$', 'campmanager.area.area'),

    url(r'^user/newlogin/$', 'campmanager.user.newlogin'),
    url(r'^user/profile/(?P<username>[\w\s\.-]+)/$', 'campmanager.user.profile'),
    url(r'^user/profile/$', 'campmanager.user.myprofile'),
    url(r'^user/login/$', 'campmanager.user.login'),
    url(r'^user/logout/$', 'campmanager.user.logoff'),
    url(r'^user/login_error/', 'campmanager.user.login_error'),
    url(r'^user/login_created/', 'campmanager.user.login_created'),
    url(r'^user/disconnected/', 'campmanager.user.disconnected'),

    url(r'^help/', 'campmanager.user.help'),
)
