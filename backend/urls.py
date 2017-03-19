from django.conf.urls import url

from . import views

urlpatterns = [
  url(r'^$', views.index, name="index"),
  url(r'^bloomers/', views.bloomers, name="bloomers"),
  url(r'^bloomer_details/(?P<username>[0-9A-Za-z]+)/$', views.bloomer_details, name="bloomer_details"),
  url(r'^classrooms/', views.classrooms, name="classrooms"),
  url(r'^classroom_details/(?P<serial>[0-9A-Za-z]+)/$', views.classroom_details, name="classroom_details"),
  url(r'^topics/', views.topics, name="topics"),
  url(r'^topic_details/(?P<pk>[0-9A-Za-z]+)/$', views.topic_details, name="topic_details"),
  #url(r'^topics_info/$', views.topics_info, name="topics_info"),
  #url(r'^topic_questions/(?P<topic_serial>[0-9A-Z]+)/$', views.topic_questions, name="topic_questions"),
  #url(r'^tools/add_questionmultiple/$', views.tools_add_questionmultiple, name="tools_add_questionmultiple"),
]
