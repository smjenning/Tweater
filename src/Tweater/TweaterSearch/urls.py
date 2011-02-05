from django.conf.urls.defaults import *
#from django.views.generic import DetailView, ListView
from TweaterSearch.views import *

urlpatterns = patterns('TweaterSearch.views',

    (r'^$', 'index'),
    (r'^admin/(?P<SearchTerm_id>\d+)/$', 'termadmin'),
    url(r'^search/(?P<SearchTerm_id>\d+)/$', 'search', name="search"),
    url(r'^rawsearch/(?P<SearchTerm_id>\d+)/$', 'rawsearch', name="rawsearch"),
    url(r'^edit/(?P<SearchTerm_id>\d+)/$', 'edit', name="edit"),
    url(r'^keywords/(?P<SearchTerm_id>\d+)/$', 'keywordformsetfactory', name="keywordformsetfactory"),
    #url(r'^deletekeyword/(?P<id>\d+)/$', 'deletekeyword', name="deletekeyword"),
    #url(r'^updatekeyword/(?P<id>\d+)/$', 'updatekeyword', name="updatekeyword"),
    url(r'^updatesearchterm/(?P<id>\d+)/$', 'updatesearchterm', name="updatesearchterm"),
    url(r'^termform/(?P<SearchTerm_id>\d+)/$', 'termform', name="termform"),

)
