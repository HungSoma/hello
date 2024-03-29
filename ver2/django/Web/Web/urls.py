"""Web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls import include ,url
from django.conf.urls.static import static
from django.contrib import admin
from login import views as auth_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', auth_views.login_view, name="login"),
    url(r'^register/$', auth_views.register, name="register"),
    url(r'^logout/$', auth_views.logout_view, name="logout"),
    url(r'^$', auth_views.home, name="home"),
    url(r'^password_reset/$',auth_views.password_reset, name="password_reset"),
    url(r'^password_reset/done/$',auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset_password/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',auth_views.password_reset_change, name='password_reset_change'),
    url(r'^reset_password/confirm/done/$', auth_views.password_reset_change_done, name="password_reset_change_done"),
    url(r'^accounts/', include('allauth.urls')),

    ]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root = settings.STATIC_ROOT)