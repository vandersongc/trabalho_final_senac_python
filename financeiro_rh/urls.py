from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Rota raiz (página inicial) -> Chama views.home
    path('',views.home, name='home'),
    
    # Rotas institucionais e de autenticação
    path('sobre/',views.sobre, name='sobre'),
    path('login/',views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('contato',views.contato, name='contato'),
    
    
    # Rotas de funcionalidade (Cálculos)
    path('calcular-rh/', views.calcular_rh, name='calcular_rh'), # Menu de cálculos
    path('contracheque/', views.contracheque, name='contracheque'), # Tela de Contracheque
    path('rescisao/', views.rescisao, name='rescisao'), # Tela de Rescisão
]