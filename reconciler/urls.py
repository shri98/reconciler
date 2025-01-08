from django.urls import path
from . import views

urlpatterns = [
    path('', views.reconcile_view, name='reconcile'),
    path('download-template/', views.download_template, name='download_template'),
]