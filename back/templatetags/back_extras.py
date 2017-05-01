from django import template
from back.orm import *

register = template.Library()

@register.filter
def relationList(instance, attr):
    return list(getRel(instance, attr))