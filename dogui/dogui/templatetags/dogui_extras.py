from django import template
import sys
from typing import Any, Type
import urllib.parse

register = template.Library()


def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)


@register.filter
def get_type(value: Any) -> Type:
    return type(value)


@register.filter
def is_instance(value: Any, class_name) -> bool:
    value = exec(value)
    class_type = exec(class_name)
    return isinstance(value, class_type)


@register.filter
def url_escape_path(value):
    # safe=':/' tells Python: "Don't touch the protocol or the slashes"
    # This turns spaces into %20 but keeps https:// intact
    if value:
        # Encode everything EXCEPT the structural characters of a URL
        return urllib.parse.quote(value, safe=':/?&=#')
    return value