from django.conf.urls import url
from django.urls import path
from punti_interesse import views

urlpatterns = [
    path('', views.home, name='home'),

    # Admin only views
    path('export/', views.export_csv, name='export'),
    path('remove-invalid-points/', views.remove_invalid_points, name='remove_invalid_points'),

    path('nuovo/', views.new, name='new'),
    path('index/<slug:slug>/', views.show, name='show'),
    path('index/<slug:slug>/modifica/', views.edit, name='edit'),
    path('index/<slug:slug>/valida/', views.validate, name='validate'),
    path('ajax/load-subcategories/', views.load_subcategories, name='ajax_load_subcategories'),

]

handler404 = views.handler404
handler500 = views.handler500
