# in your app's templatetags directory, create a file called `custom_filters.py`
from django import template

register = template.Library()

@register.filter
def get_attribute(obj, attr_name):
    return getattr(obj, attr_name)

# templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.simple_tag
def active(request, pattern):
    path = request.path
    if path == pattern:
        return 'active'
    return ''