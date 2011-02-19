from django.conf.urls.defaults import *
#from TweaterSearch.views import *
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^Tweater/', include('Tweater.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^TweaterSearch/', include('TweaterSearch.urls')),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.MEDIA_ROOT } ),
    (r'^accounts/', include('registration.urls')),
)
