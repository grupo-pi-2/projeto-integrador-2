from django.urls import path
from . import views

from usuarios.views import  cadastro_view, editar_perfil_view, login_view

from django.contrib import admin

from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('usuarios/logout/', LogoutView.as_view(next_page='/usuarios/login/'), name='logout'),
    path('editar_perfil/', editar_perfil_view, name='editar_perfil'),
    path('index/', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('usuarios/login/', login_view, name='login'),
    path('usuarios/cadastro/', cadastro_view, name='cadastro'),  
    path('', views.index, name='index'),
    path('busca_indicador/<int:indicador_id>/', views.busca_indicador, name='busca_indicador'),
    path('lista_clientes/', views.lista_clientes, name='lista_clientes'),
    path('lista_status_servico/', views.lista_status_servico, name='lista_status_servico'),
    path('cria_servico/', views.cria_servico, name='cria_servico'),
    path('atualiza_servico/<int:servico_id>/', views.atualiza_servico, name='atualiza_servico'),
    path('exclui_servico/<int:servico_id>/', views.exclui_servico, name='exclui_servico'),
    path('busca_servico/<int:servico_id>/', views.busca_servico, name='busca_servico'),
    path('clientes/', views.clientes, name='clientes'),
    path('cria_cliente/', views.cria_cliente, name='cria_cliente'),
    path('atualiza_cliente/<int:cliente_id>/', views.atualiza_cliente, name='atualiza_cliente'),
    path('exclui_cliente/<int:cliente_id>/', views.exclui_cliente, name='exclui_cliente'),
    path('busca_cliente/<int:cliente_id>/', views.busca_cliente, name='busca_cliente'),
    path('lista_responsaveis/', views.lista_responsaveis, name='lista_responsaveis'),
]
