from django import template

register = template.Library()

@register.filter
def fltr_scorebloomertopic(obj, epk):
    return obj.get_scorevalue_of(epk)