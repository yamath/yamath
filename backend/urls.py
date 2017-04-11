from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^bloomers/', views.bloomers, name="bloomers"),
    url(r'^bloomer_details/(?P<username>[0-9A-Za-z]+)/$', views.bloomer_details, name="bloomer_details"),
    url(r'^classrooms/', views.classrooms, name="classrooms"),
    url(r'^classroom_details/(?P<name>[0-9A-Za-z]+)/$', views.classroom_details, name="classroom_details"),
    url(r'^envelopes/', views.envelopes, name='envelopes'),
    url(r'^sendEnvelope/', views.sendEnvelope, name="sendEnvelope"),
    url(r'^series/', views.series, name="series"),
    url(r'^serie_details/(?P<serieSerial>[0-9A-Za-z]+)/$', views.serie_details, name="serie_details"),
    url(r'^serie_new/', views.serie_new, name="serie_new"),
    url(r'^topic_details/(?P<topicSerial>[0-9A-Za-z]+)/$', views.topic_details, name="topic_details"),
    url(r'^topic_new/(?P<serieSerial>[0-9A-Za-z]+)/$', views.topic_new, name="topic_new"),
    url(r'^question_details/(?P<questionSerial>[0-9A-Za-z]+)/$', views.question_details, name="question_details"),
    url(r'^question_new/(?P<topicSerial>[0-9A-Za-z]+)/$', views.question_new, name="question_new"),
    url(r'^option_details/(?P<optionSerial>[0-9A-Za-z]+)/$', views.option_details, name="option_details"),
    url(r'^option_new/(?P<questionSerial>[0-9A-Za-z]+)/$', views.option_new, name="option_new"),
    url(r'^copy/(?P<oldSerial>[0-9A-Za-z]+)-(?P<newSerial>[0-9A-Za-z]+)/$', views.copy, name="copy"),
    url(r'^delete/(?P<serial>[0-9A-Za-z]+)/$', views.delete, name="delete"),
    ###
    url(r'^claim/$', views.claim, name="claim"),
    url(r'^claim_solved/(?P<claim_pk>[0-9A-Za-z]+)/$', views.claim_solved, name="claim_solved"),
    url(r'^claims/$', views.claims, name="claims"),
    url(r'^create_bulk_bool/$', views.create_bulk_bool, name="create_bulk_bool"),
    url(r'^create_multi/$', views.create_multi, name="create_multi"),
    url(r'^create_topic/$', views.create_topic, name="create_topic"),
    url(r'^new_question/', views.new_question, name="new_question"),
    url(r'^pendings/', views.pendings, name="pendings"),
    url(r'^pending_details/(?P<option_pk>[0-9A-Za-z]+)/', views.pending_details, name="pending_details"),
    url(r'^pending_solved/(?P<option_pk>[0-9A-Za-z]+)/', views.pending_solved, name="pending_solved"),
    #url(r'^topic_questions/(?P<topic_serial>[0-9A-Z]+)/$', views.topic_questions, name="topic_questions"),
    #url(r'^tools/add_questionmultiple/$', views.tools_add_questionmultiple, name="tools_add_questionmultiple"),
]
