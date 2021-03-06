from django.conf.urls.defaults import *
from smj_app.views import *
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
    #(r'^smj_app/', include('smj_app.urls')),
    url(r'^smj_app/$', 
        index, 
        name='index'),
    url(r'^smj_app/admin/(?P<SearchTerm_id>\d+)/$', 
        termadmin, 
        name='termadmin'),
    url(r'^smj_app/search/(?P<SearchTerm_id>\d+)/$', 
        search, 
        name="search"),
    url(r'^smj_app/rawsearch/(?P<SearchTerm_id>\d+)/$', 
        rawsearch, 
        name="rawsearch"),
    url(r'^smj_app/edit/(?P<SearchTerm_id>\d+)/$', 
        edit, 
        name="edit"),
    url(r'^smj_app/keywords/(?P<SearchTerm_id>\d+)/$', 
        keywordformsetfactory, 
        name="keywordformsetfactory"),
    url(r'^smj_app/termform/(?P<SearchTerm_id>\d+)/$', 
        termform, 
        name="termform"),
    url(r'^smj_app/term/(?P<SearchTerm_id>\d+)/$', 
        neworedit, 
        name="neworedit"),
    url(r'^smj_app/site_media/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
    url(r'^smj_app/delkw/(?P<SearchTerm_id>\d+)/(?P<kid>\d+)/$', 
        delkw, 
        name="delkw"),
    url(r'^smj_app/delst/(?P<SearchTerm_id>\d+)/$', 
        delst, 
        name="delst"),
    url(r'^smj_app/addtodo/$', 
        addtodo, 
        name="addtodo"),
    url(r'^smj_app/managetodo/$', 
        managetodo, 
        name="managetodo"),
    url(r'^smj_app/viewtodo/$', 
        viewtodo, 
        name="viewtodo"),
    url(r'^smj_app/about/$', 
        about, 
        name="about"),
    url(r'^smj_app/contact/$', 
        contact, 
        name="contact"),
   
)
