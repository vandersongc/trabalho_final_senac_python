from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.home, name='home'),
    path('sobre/',views.sobre, name='sobre'),
    path('login/',views.login, name='login'),
    path('contato',views.contato, name='contato'),
    path('admin/',views.admin, name='admin'),
    path('calcular-rh/', views.calcular_rh, name='calcular_rh'),
    path('contracheque/', views.contracheque, name='contracheque'),
    path('rescisao/', views.rescisao, name='rescisao'),
]