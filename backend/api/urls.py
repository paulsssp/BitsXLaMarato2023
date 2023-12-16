from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('upload_encuesta_pbac/', views.upload_encuesta_pbac, name='upload_encuesta'),
    path('upload_encuesta_qol/', views.upload_encuesta_qol, name='upload_encuesta_qol'),
    path('get_encuesta_pbac/<int:user_id>/', views.get_encuesta_pbac, name='get_encuesta_pbac'),
    path('get_encuesta_qol/<int:user_id>/', views.get_encuesta_qol, name='get_encuesta_qol'),
]
