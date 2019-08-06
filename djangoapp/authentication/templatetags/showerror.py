from django import template
from django.template import engines
from django.template.defaultfilters import stringfilter
import logging

register = template.Library()

logger = logging.getLogger('django')

@register.filter
@stringfilter
def showerror(value):
    template = engines['django'].from_string(value)
    result = template.render({})
    return result
