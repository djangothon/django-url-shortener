import redisco.models as r_models
import urllib2
import thread

import requests

import utils


class Link(r_models.Model):
    """Model that represents a shortened URL."""

    short_url = r_models.Attribute(unique=True)
    url = r_models.Attribute(required=True)
    date_submitted = r_models.DateTimeField(auto_now_add=True)
    usage_count = r_models.IntegerField(default=0, indexed=True)
    is_custom = r_models.BooleanField()

    def __unicode__(self):
        return '%s : %s' % (self.url, self.short_url)

    def save(self, *args, **kwargs):
        if hasattr(self, 'id'):
            super(self.__class__, self).save(*args, **kwargs)
            return

        if self.is_custom:
            pass
        else:
            self.short_url = utils.get_short_url()

        while True:
            existing_link = self.__class__.objects.filter(short_url=self.short_url)
            if existing_link:
                if self.is_custom:
                    raise ValueError('Custom url already exists')
                else:
                    self.short_url = utils.get_short
            else:
                break
        super(self.__class__, self).save(*args, **kwargs)


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
