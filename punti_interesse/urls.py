from django.conf.urls import url
from punti_interesse import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^nuovo/$', views.new, name='new'),
    url(r'^(?P<slug>[\w\-]+)/$', views.show, name='show'),
    url(r'^(?P<slug>[\w\-]+)/modifica/$', views.edit, name='edit'),
    url(r'^(?P<slug>[\w\-]+)/valida/$', views.validate, name='validate'),
]

handler404 = views.handler404
handler500 = views.handler500