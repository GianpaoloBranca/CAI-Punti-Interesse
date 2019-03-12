from django.conf.urls import url
from punti_interesse import views

urlpatterns = [
    url(r'^$', views.home, name='home'),

    # Non-CAS authentication views (to be removed soon)
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),

    # Admin only views
    url(r'^export/$', views.export_csv, name='export'),
    url(r'^remove-invalid-points/$', views.remove_invalid_points, name='remove_invalid_points'),

    url(r'^nuovo/$', views.new, name='new'),
    url(r'^index/(?P<slug>[\w\-]+)/$', views.show, name='show'),
    url(r'^index/(?P<slug>[\w\-]+)/modifica/$', views.edit, name='edit'),
    url(r'^index/(?P<slug>[\w\-]+)/valida/$', views.validate, name='validate'),
    url(r'^ajax/load-subcategories/$', views.load_subcategories, name='ajax_load_subcategories'),

]

handler404 = views.handler404
handler500 = views.handler500
