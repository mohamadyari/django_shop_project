from django import template

register = template.Library()


@register.simple_tag()
def filter_url(number, name, urlencode=None):
    url = '?{}={}'.format(name, number)
    if urlencode:
        sp_query = urlencode.split('&')
        sp_filter = filter(lambda x: x.split('=')[0] != name, sp_query)
        join_query = '&'.join(sp_filter)
        url = '{}&{}'.format(url, join_query)
    return url
