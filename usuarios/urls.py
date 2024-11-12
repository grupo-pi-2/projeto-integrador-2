# usuarios/urls.py
from django.urls import path
from .views import login_view, cadastro_view # Verifique se os nomes estão corretos
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', login_view, name='login'),
    path('cadastro/', cadastro_view, name='cadastro'),
    path('logout/', LogoutView.as_view(next_page='/usuarios/login/'), name='logout'), 
]
