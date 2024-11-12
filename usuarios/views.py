# usuarios/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import CustomAuthenticationForm, CustomUserCreationForm

def login_view(request):
    # Verifica se o usuário já está autenticado
    if request.user.is_authenticated:
        return redirect('index')  # Se já estiver logado, redireciona para o index

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)  # Realiza o login do usuário
                return redirect('index')  # Redireciona para o index após o login
            else:
                messages.error(request, 'Credenciais inválidas')  # Mensagem de erro caso as credenciais sejam inválidas
        else:
            messages.error(request, 'Formulário inválido')  # Mensagem de erro caso o formulário não seja válido
    else:
        form = CustomAuthenticationForm()

    return render(request, 'usuarios/login.html', {'form': form})

def cadastro_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')  # Redireciona para a página inicial após o cadastro
        messages.error(request, 'Erro ao criar conta. Verifique os dados.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'usuarios/cadastro.html', {'form': form}) 