from django import template
from django.conf import settings

register = template.Library()


@register.assignment_tag
def get_setting(param):
    return getattr(settings, param, None)
