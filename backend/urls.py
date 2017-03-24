from django.conf.urls import url

from . import views

urlpatterns = [
  url(r'^$', views.index, name="index"),
  url(r'^bloomers/', views.bloomers, name="bloomers"),
  url(r'^bloomer_details/(?P<username>[0-9A-Za-z]+)/$', views.bloomer_details, name="bloomer_details"),
  url(r'^claim/$', views.claim, name="claim"),
  url(r'^claim_solved/(?P<claim_pk>[0-9A-Za-z]+)/$', views.claim_solved, name="claim_solved"),
  url(r'^claims/$', views.claims, name="claims"),
  url(r'^classrooms/', views.classrooms, name="classrooms"),
  url(r'^classroom_details/(?P<serial>[0-9A-Za-z]+)/$', views.classroom_details, name="classroom_details"),
  url(r'^new_question/', views.new_question, name="new_question"),
  url(r'^pendings/', views.pendings, name="pendings"),
  url(r'^pending_details/(?P<option_pk>[0-9A-Za-z]+)/', views.pending_details, name="pending_details"),
  url(r'^pending_solved/(?P<option_pk>[0-9A-Za-z]+)/', views.pending_solved, name="pending_solved"),
  #url(r'^question_details/', views.question_details, name="question_details"),
  url(r'^question_details/(?P<question_pk>[0-9a-zA-Z]+)/', views.question_details, name="question_details"),
  url(r'^topics/', views.topics, name="topics"),
  url(r'^topic_details/(?P<pk>[0-9A-Za-z]+)/$', views.topic_details, name="topic_details"),
  #url(r'^topic_questions/(?P<topic_serial>[0-9A-Z]+)/$', views.topic_questions, name="topic_questions"),
  #url(r'^tools/add_questionmultiple/$', views.tools_add_questionmultiple, name="tools_add_questionmultiple"),
]
