from django import template
import sys
from typing import Any, Type

register = template.Library()


def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)


@register.filter
def get_type(value: Any) -> Type:
    return type(value)


@register.filter
def is_instance(value: Any, class_name) -> bool:
    class_type: Type = exec(class_name)
    return isinstance(value, class_type)
