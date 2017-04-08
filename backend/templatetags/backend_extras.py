from django import template
from content.models import *
from bloomerprofile.models import *

register = template.Library()

@register.filter
def bsMean(b, s):
    return b.get_mean_of_serie(s)

@register.filter
def btMean(b, t):
    return b.get_mean_of_topic(t)

@register.filter
def getClassroomsOfSerie(s):
    return [ c for c in Classroom.objects.all() if s in c.series ]