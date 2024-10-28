from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('busca_indicador/<int:indicador_id>/', views.busca_indicador, name='busca_indicador'),
    path('lista_clientes/', views.lista_clientes, name='lista_clientes'),
    path('lista_status_servico/', views.lista_status_servico, name='lista_status_servico'),
    path('cria_servico/', views.cria_servico, name='cria_servico'),
    path('atualiza_servico/<int:servico_id>/', views.atualiza_servico, name='atualiza_servico'),
    path('exclui_servico/<int:servico_id>/', views.exclui_servico, name='exclui_servico'),
    path('busca_servico/<int:servico_id>/', views.busca_servico, name='busca_servico'),
]
