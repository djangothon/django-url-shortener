from redisco import models

from shortener.baseconv import base62


class Link(models.Model):
    """
    Model that represents a shortened URL
    """
    url = models.Attribute(required=True)
    date_submitted = models.DateTimeField(auto_now_add=True)
    usage_count = models.PositiveIntegerField(default=0, indexed=True)

    def to_base62(self):
        return base62.from_decimal(self.id)

    def __unicode__(self):
        return '%s : %s' % (self.to_base62(), self.url)

    class Meta:
        get_latest_by = 'date_submitted'
