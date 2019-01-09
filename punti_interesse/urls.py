from django.conf.urls import url
from punti_interesse import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
