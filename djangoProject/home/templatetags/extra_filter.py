from django import template

register = template.Library()


@register.filter()
def upper_name(value):
    return value.upper()
