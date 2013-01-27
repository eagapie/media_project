'''
@author elena
url mappings for mediacloud
'''

from django.conf.urls.defaults       import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from mediacloud                      import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^media/(?P<media_id>\d+)/$', views.detail_media, name='detail_media'),
    url(r'^story/(?P<story_id>\d+)/$', views.detail_story, name='detail_story'),
#    url(r'^search/$', views.search, name='search'),
#    url(r'^search_form/$', views.search_form, name='search_form'),
    url(r'^search_cat/$', views.search_cat, name='search_cat'),
    url(r'^search_cat_results/$', views.search_cat_results, name='search_cat_results'),
    url(r'^search_results_wikileaks/$', views.search_results_wikileaks, name='search_results_wikileaks'),
)


urlpatterns += staticfiles_urlpatterns()
