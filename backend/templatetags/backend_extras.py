from django import template

register = template.Library()

@register.filter
def bsMean(b, s):
    return b.get_mean_of_serie(s)

@register.filter
def btMean(b, t):
    return b.get_mean_of_topic(t)