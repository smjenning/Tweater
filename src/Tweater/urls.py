from django.conf.urls.defaults import *
from TweaterSearch.views import *
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', 
     include(admin.site.urls)),       
    url(r'^site_media/(?P<path>.*)$', 
        'django.views.static.serve', 
        { 'document_root': settings.MEDIA_ROOT } ),
    url(r'^accounts/', 
        include('registration.urls')),    
    #(r'^TweaterSearch/', include('TweaterSearch.urls')),
    url(r'^TweaterSearch/$', 
        index, 
        name='index'),
    url(r'^TweaterSearch/admin/(?P<SearchTerm_id>\d+)/$', 
        termadmin, 
        name='termadmin'),
    url(r'^TweaterSearch/search/(?P<SearchTerm_id>\d+)/$', 
        search, 
        name="search"),
    url(r'^TweaterSearch/rawsearch/(?P<SearchTerm_id>\d+)/$', 
        rawsearch, 
        name="rawsearch"),
    url(r'^TweaterSearch/edit/(?P<SearchTerm_id>\d+)/$', 
        edit, 
        name="edit"),
    url(r'^TweaterSearch/keywords/(?P<SearchTerm_id>\d+)/$', 
        keywordformsetfactory, 
        name="keywordformsetfactory"),
    url(r'^TweaterSearch/termform/(?P<SearchTerm_id>\d+)/$', 
        termform, 
        name="termform"),
    url(r'^TweaterSearch/term/(?P<SearchTerm_id>\d+)/$', 
        neworedit, 
        name="neworedit"),
    url(r'^TweaterSearch/site_media/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
    url(r'^TweaterSearch/delkw/(?P<SearchTerm_id>\d+)/(?P<kid>\d+)/$', 
        delkw, 
        name="delkw"),
    url(r'^TweaterSearch/delst/(?P<SearchTerm_id>\d+)/$', 
        delst, 
        name="delst"),
    
)
