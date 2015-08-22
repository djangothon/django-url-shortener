from django.http import HttpResponsePermanentRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET, require_POST

from shortener.baseconv import base62
from shortener.models import Link, LinkAccess
from shortener.forms import LinkSubmitForm
from shortener.utils import get_ip_from_request


@require_GET
def follow(request, base62_id):
    """
    View which gets the link for the given base62_id value
    and redirects to it.
    """
    link = Link.objects.get_by_id(base62.to_decimal(base62_id))
    if not link:
        raise Http404('No Link found')
    link.usage_count += 1
    link.save()

    # write into LinkAccess
    LinkAccess.objects.create(link=link,
                              referrer=request.META.get('HTTP_REFERRER'),
                              ip=get_ip_from_request(request))

    return HttpResponsePermanentRedirect(link.url)


@require_GET
def info(request, base62_id):
    """
    View which shows information on a particular link
    """
    link = Link.objects.get_by_id(base62.to_decimal(base62_id))
    if not link:
        raise Http404('No Link found')
    return render(request, 'shortener/link_info.html', {'link': link})


@require_POST
def submit(request):
    """
    View for submitting a URL to be shortened
    """
    form = LinkSubmitForm(request.POST)
    if form.is_valid():
        kwargs = {'url': form.cleaned_data['url']}
        custom = form.cleaned_data['custom']
        if custom:
            # specify an explicit id corresponding to the custom url
            kwargs.update({'id': base62.to_decimal(custom)})
        link = Link.objects.create(**kwargs)
        print link
        return render(request, 'shortener/submit_success.html', {'link': link})
    else:
        return render(request, 'shortener/submit_failed.html', {'link_form': form})


@require_GET
def index(request):
    """
    View for main page
    """
    values = {
        'link_form': LinkSubmitForm(),
        'recent_links': Link.objects.all()[:5],
        'most_popular_links': Link.objects.all()[:5]}
    return render(request, 'shortener/index.html', values)
