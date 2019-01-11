from django.conf.urls import url
from punti_interesse import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ril/', views.rilevatore, name='rilevatore'),
    url(r'^val/', views.validatore, name='validatore'),
]
