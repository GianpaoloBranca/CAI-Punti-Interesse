from django.conf.urls import url
from punti_interesse import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ril/$', views.rilevatore, name='rilevatore'),
    url(r'^val/$', views.validatore, name='validatore'),
    url(r'^ril/(?P<pi_name_slug>[\w\-]+)/$', views.show_pi_ril, name='show_pi_ril'),
    url(r'^ril/(?P<pi_name_slug>[\w\-]+)/edit', views.edit_pi, name='edit_pi'),
]
