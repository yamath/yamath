from django.conf.urls import url

from . import views

urlpatterns = [
  url(r'^$', views.index, name="index"),
  url(r'^topics_info/$', views.topics_info, name="topics_info"),
  url(r'^topic_questions/(?P<topic_serial>[0-9A-Z]+)/$', views.topic_questions, name="topic_questions"),
  #url(r'^tools/add_questionmultiple/$', views.tools_add_questionmultiple, name="tools_add_questionmultiple"),
]
