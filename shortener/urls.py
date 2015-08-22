from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('shortener.views',
    url(r'^$', 'index', name='index'),
    url(r'^info/(?P<link_id>\w+)$', 'info', name='info'),
    url(r'^submit/$', 'submit', name='submit'),
    url(r'^link_access_map/$', 'access_map', name='map_access'),
    url(r'^(?P<short_url>.*)$', 'follow', name='follow'),
)
