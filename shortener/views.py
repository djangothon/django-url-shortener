from django.http import HttpResponsePermanentRedirect, Http404
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST

from shortener.models import Link, LinkAccess
from shortener.forms import LinkSubmitForm
from shortener.utils import get_ip_from_request


@require_GET
def follow(request, short_url):
    """
    View which gets the link for the given short url
    and redirects to it.
    """
    link_set = Link.objects.filter(short_url=short_url)
    if link_set:
        link = link_set[0]
        link.usage_count += 1
        link.save()
        # write into LinkAccess
        LinkAccess.objects.create(link=link,
                                  referrer=request.META.get('HTTP_REFERRER'),
                                  ip=get_ip_from_request(request))

        return HttpResponsePermanentRedirect(link.url)
    else:
        raise Http404('No Link found')


@require_GET
def info(request, link_id):
    """
    View which shows information on a particular link
    """
    link = Link.objects.get_by_id(link_id)
    if link:
        return render(request, 'link_info.html', {'link': link})
    else:
        raise Http404('No Link found')


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
            kwargs.update({'is_custom': True, 'short_url': custom})
        link = Link(**kwargs)
        link.save()
        return render(request, 'submit_success.html', {'link': link})
    else:
        return render(request, 'submit_failed.html', {'link_form': form})


@require_GET
def index(request):
    """View for main page"""
    values = {
        'link_form': LinkSubmitForm(),
        'recent_links': Link.objects.all()[:5],
        'most_popular_links': Link.objects.all()[:5]
    }
    return render(request, 'index.html', values)

@require_GET
def access_map(request):
    ctx = {}
    template_name = 'map_box.html'
    return render(request, template_name, ctx)
