"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from usuarios.views import path
from django.contrib.auth.views import LogoutView
from usuarios.views import login_view

urlpatterns = [
    path('usuarios/login/', login_view, name='login'),
    path('admin/', admin.site.urls),
    path('gestao_de_indicadores', include("gestao_de_indicadores.urls")),
    path('admin/', admin.site.urls),
    path('usuarios/', include('usuarios.urls')),
    path('', include('gestão_de_indicadores.urls')),  # Página principal
    path('logout/', LogoutView.as_view(next_page='/usuarios/login/'), name='logout'),
]
