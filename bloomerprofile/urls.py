from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r'^$', views.index, name="index"),
    url(r'^ajax/$', views.ajax, name='ajax'),
    url(r'^ajax/loadDoneSeries/$', views.loadDoneSeries, name='loadDoneSeries'),
    url(r'^ajax/loadTodoSeries/$', views.loadTodoSeries, name='loadTodoSeries'),
    url(r'^ajax/loadLateSeries/$', views.loadLateSeries, name='loadLateSeries'),
    url(r'^ajax/loadQuestionText/$', views.loadQuestionText, name='loadQuestionText'),
    url(r'^ajax/loadQuestionForm/$', views.loadQuestionForm, name='loadQuestionForm'),
    url(r'^ajax/chooseQuestion/$', views.chooseQuestion, name='chooseQuestion'),
    url(r'^ajax/submitAnswer/$', views.submitAnswer, name='submitAnswer'),
    url(r'^ajax/unansweredQuestion/$', views.unansweredQuestion, name='unansweredQuestion'),
    # url(r'^ajax/selectSerie/$', views.selectSerie, name='selectSerie'),
    # url(r'^submit/$', views.submit, name="submit"),
    # url(r'^(?P<topic_pk>[0-9A-Z]+)/$', views.question, name="question"),
]