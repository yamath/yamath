from django.conf.urls import url

from . import views
from back import views as back_views

urlpatterns = [
    url(r'^$', views.main, name="main"),
    url(r'^html/(?P<query>.+)$', views.html, name="html"),
    url(r'^back/(?P<query>.+)$', back_views.back, name="back"),
]