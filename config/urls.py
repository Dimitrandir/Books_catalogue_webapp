"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
"""
import re

from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path, re_path
from django.views.static import serve as serve_static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', include('loans.urls')),
    path('', include('scanner.urls')),
    path('', include('catalog.urls')),
]

# Media (Railway Volume, локален диск) — сервира се директно от Django,
# понеже нямаме отделен CDN/reverse proxy пред media файловете (static/
# минава през whitenoise, но това покрива само static). Django's serve()
# view не е оптимизиран за голям production трафик, но е напълно
# достатъчен за малка семейна библиотека.
#
# Умишлено НЕ ползваме django.conf.urls.static.static() тук — тя вътрешно
# проверява settings.DEBUG и връща [] (нищо не се регистрира) при
# DEBUG=False, независимо дали извикването отвън е обвито в `if DEBUG`.
# Затова regex route-ът е добавен директно, за да работи и в production.
urlpatterns += [
    re_path(
        r'^%s(?P<path>.*)$' % re.escape(settings.MEDIA_URL.lstrip('/')),
        serve_static,
        {'document_root': settings.MEDIA_ROOT},
    ),
]
