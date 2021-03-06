"""yamath URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from blooming.views import index, login_view

urlpatterns = [
    url(r'^$', index, name='main'),
    url(r'^login/$', login_view),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^bloomerprofile/', include('bloomerprofile.urls', namespace='bloomerprofile')),
    url(r'^backend/', include('backend.urls', namespace='backend')),
    url(r'^blooming/', include('blooming.urls', namespace='blooming')),
    url(r'^experimental/', include('look.urls', namespace='look')),
]
