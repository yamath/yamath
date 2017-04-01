from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^profile/$', views.profile, name='profile'),
    # url(r'^submit/$', views.submit, name="submit"),
    # url(r'^(?P<topic_pk>[0-9A-Z]+)/$', views.question, name="question"),
]
