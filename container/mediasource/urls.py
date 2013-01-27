from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'links.views.home', name='home'),
    # url(r'^links/', include('links.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/',      include(admin.site.urls)),
    url(r'^media/', include('mediacloud.urls')),
    url(r'^wikileaks/',  include('wikileaks.urls')),
    #url(r'^search/', include('search.urls')),
)
