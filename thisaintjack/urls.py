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
    url(r'^bigshit/$', 'campmanager.views.bigshitlist'),

    url(r'^subcamp/(?P<subcamp>\w+)/$', 'campmanager.views.subcamp'),
    url(r'^campsite/(?P<siteid>\d+)/$', 'campmanager.campsite.campsite'),
    url(r'^campsite/(?P<siteid>\d+)/bigshit/(?P<shitid>\d+)/$', 'campmanager.area.area'),

    url(r'^user/newlogin/$', 'campmanager.user.newlogin'),
    url(r'^user/profile/(?P<username>\w+)/$', 'campmanager.user.profile'),
    url(r'^user/profile/$', 'campmanager.user.myprofile'),
    url(r'^user/login/$', 'campmanager.user.login'),
    url(r'^user/logout/$', 'campmanager.user.logoff'),
    url(r'^user/login_error/', 'campmanager.user.login_error'),
    url(r'^user/login_created/', 'campmanager.user.login_created'),

    url(r'^help/', 'campmanager.user.help'),
)
