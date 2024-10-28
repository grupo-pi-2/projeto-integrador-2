from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('busca_indicador/<int:indicador_id>/', views.busca_indicador, name='busca_indicador'),
    path('lista_clientes/', views.lista_clientes, name='lista_clientes'),
    path('lista_status_servico/', views.lista_status_servico, name='lista_status_servico'),
    path('salva_servico/', views.salva_servico, name='salva_servico'),
]
