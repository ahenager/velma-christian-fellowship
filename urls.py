from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
import settings

admin.autodiscover()

from django.contrib.flatpages.views import flatpage

urlpatterns = patterns('',
    # Example:
    # (r'^vcf/', include('vcf.foo.urls')),
    (r'^$', flatpage, { 'url' : 'home/' } ),
    (r'^audio/$', 'vcf.audio_manager.views.search'),
    (r'^directory/$', 'vcf.family_manager.views.search'),
    (r'^directory/print/$', 'vcf.family_manager.views.print_directory'),
    (r'^audio/clean/$', 'vcf.audio_manager.views.clean'),
    (r'^audio/import/$', 'vcf.audio_manager.views.import_audio'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^verify/$', 'django.contrib.auth.views.login', {'template_name': 'verify.html'}),
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    from django.views.static import serve
    _media_url = settings.MEDIA_URL
    if _media_url.startswith('/'):
        _media_url = _media_url[1:]
        urlpatterns += patterns('',
                                 (r'^%s(?P<path>.*)$' % _media_url,
                                 serve,
                                 {'document_root': settings.MEDIA_ROOT}))
    del(_media_url, serve)