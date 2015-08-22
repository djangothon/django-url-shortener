from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('shortener.views',
    url(r'^$', 'index', name='index'),
    url(r'^info/(?P<base62_id>.*)$', 'info', name='info'),
    url(r'^submit/$', 'submit', name='submit'),
    url(r'^(?P<base62_id>.*)$', 'follow', name='follow'),
)
