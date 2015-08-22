from urlparse import urlparse

from django import forms

from shortener.models import Link


too_long_error = "Your custom name is too long. Are you sure you wanted a shortening service? :)"


class LinkSubmitForm(forms.Form):
    url = forms.URLField(label='URL to be shortened',)
    custom = forms.CharField(label='Custom shortened name',
                             required=False,)

    def clean_custom(self):
        custom = self.cleaned_data['custom']
        if not custom:
            return

        parsed_url = urlparse(custom)
        if parsed_url.netloc:
            raise forms.ValidationError('Do not input the domain, '
                                        'only the unique part of url')
        try:
            if Link.objects.filter(short_url=custom):
                raise forms.ValidationError('"%s" is already taken' % custom)
        except OverflowError:
            raise forms.ValidationError(too_long_error)
        return custom
