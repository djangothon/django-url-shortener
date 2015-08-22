import urllib2

import requests
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from shortener.baseconv import base62


class Link(models.Model):

    """Model that represents a shortened URL."""

    url = models.URLField()
    date_submitted = models.DateTimeField(auto_now_add=True)
    usage_count = models.PositiveIntegerField(default=0)

    def to_base62(self):
        return base62.from_decimal(self.id)

    def __unicode__(self):
        return '%s : %s' % (self.to_base62(), self.url)

    class Meta:
        get_latest_by = 'date_submitted'


class LinkAccess(models.Model):

    """Model that represents access of a shortened url."""

    link = models.ForeignKey(Link)
    country = models.CharField(max_length=80, null=True)
    region = models.CharField(max_length=128, null=True)
    referrer = models.CharField(max_length=256, null=True)
    lat = models.CharField(max_length=16, null=True)
    lng = models.CharField(max_length=16, null=True)
    ip = models.CharField(max_length=32, null=True)
    atime = models.DateTimeField(auto_now_add=True)


@receiver(post_save, sender=LinkAccess)
def geotag_link_access(sender, **kwargs):
    """
    Add geolocation info to link access.

    Get geolocation info by passing client ip to the freegeoip API.
    """
    la = kwargs['instance']

    if la.ip:
        url = 'https//freegeoip.net/json/{0}'.format(urllib2.quote(la.ip))
    else:
        return
    response = requests.get(url)

    if response.ok:
        response_data = response.json()
        la.country = response_data.get('country_name')
        la.region = response_data.get('region_name')
        la.lat = response_data.get('latitude')
        la.lng = response_data.get('longitude')
        la.save()
