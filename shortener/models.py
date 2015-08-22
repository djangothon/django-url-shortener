import redisco.models as r_models
import urllib2
import thread

import requests

from shortener.baseconv import base62


class Link(r_models.Model):
    """Model that represents a shortened URL."""

    url = r_models.Attribute(required=True)
    date_submitted = r_models.DateTimeField(auto_now_add=True)
    usage_count = r_models.IntegerField(default=0, indexed=True)

    def to_base62(self):
        return base62.from_decimal(int(self.id))

    def __unicode__(self):
        return '%s : %s' % (self.to_base62(), self.url)


class LinkAccess(r_models.Model):

    """Model that represents access of a shortened url."""

    link = r_models.ReferenceField(Link)
    country = r_models.Attribute()
    region = r_models.Attribute()
    referrer = r_models.Attribute()
    lat = r_models.Attribute()
    lng = r_models.Attribute()
    ip = r_models.Attribute()
    atime = r_models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super(LinkAccess, self).save(*args, **kwargs)
        thread.start_new_thread(geotag_link_access, (self, True))


def geotag_link_access(instance, created):
    """
    Add geolocation info to link access.

    Get geolocation info by passing client ip to the freegeoip API.
    """
    la = instance

    if la.ip:
        url = 'https://freegeoip.net/json/{0}'.format(urllib2.quote(la.ip))
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
