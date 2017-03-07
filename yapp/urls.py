from django.conf.urls import url

from . import views

urlpatterns = [
  url(r'^$', views.index, name="index"),
  url(r'^3M/$', views.index_3M, name="terza_media"),
  url(r'^1A/$', views.index_1A, name="prima_artistico"),
  url(r'^2A/$', views.index_2A, name="seconda_artistico"),
  url(r'^2S/$', views.index_2S, name="seconda_scientifico"),
  url(r'^(?P<topic_serial>[0-9A-Z]+)/$', views.question, name="question"),
]
