from django.conf.urls import url

from . import views

urlpatterns = [
  url(r'^$', views.index, name="index"),
  url(r'^(?P<topic_serial>[0-9A-Z]+)/$', views.question, name="question"),
]
