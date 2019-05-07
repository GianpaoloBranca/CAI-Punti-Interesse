from django.conf.urls import include
from django.urls import path
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

import django_cas_ng.views

urlpatterns = [
    path('', include('punti_interesse.urls')),
    path('admin/', admin.site.urls, name='admin'),
    # CAS paths
    path('accounts/cas-login/', django_cas_ng.views.LoginView.as_view(), name='cas_ng_login'),
    path('accounts/cas-logout/', django_cas_ng.views.LogoutView.as_view(), name='cas_ng_logout'),
    path('accounts/callback/', django_cas_ng.views.CallbackView.as_view(), name='cas_ng_proxy_callback'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
