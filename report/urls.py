"""report URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url, include
from django.urls import path
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

import django_cas_ng.views

from punti_interesse import views

urlpatterns = [
    path('', views.home, name='home'),
    path('pi/', include('punti_interesse.urls')),
    path('admin/', admin.site.urls, name='admin'),
    # CAS URLs
    path('accounts/cas-login/', django_cas_ng.views.LoginView.as_view(), name='cas_ng_login'),
    path('accounts/cas-logout/', django_cas_ng.views.LogoutView.as_view(), name='cas_ng_logout'),
    path('accounts/callback/', django_cas_ng.views.CallbackView.as_view(), name='cas_ng_proxy_callback'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
