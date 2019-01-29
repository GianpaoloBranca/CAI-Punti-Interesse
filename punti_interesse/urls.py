from django.conf.urls import url
from punti_interesse import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^nuovo/$', views.new, name='new'),
    url(r'^(?P<pi_name_slug>[\w\-]+)/$', views.show, name='show'),
    url(r'^(?P<pi_name_slug>[\w\-]+)/modifica/$', views.edit, name='edit'),
]
