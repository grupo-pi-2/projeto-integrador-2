from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('busca_indicador/<int:indicador_id>/', views.busca_indicador, name='busca_indicador'),
]
