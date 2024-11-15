# usuarios/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib import messages
from .forms import CustomAuthenticationForm, CustomUserCreationForm, EditProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm



@login_required
def editar_perfil_view(request):
    user = request.user
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            # Checa se a senha foi preenchida e faz update
            new_password = form.cleaned_data.get('password')
            if new_password:
                user.set_password(new_password)  # Atualiza a senha
            user.save()  # Salva o perfil atualizado
            update_session_auth_hash(request, user)  # Garante que o usuário permanece logado após mudar a senha
            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect('index')  # Redireciona após a edição
        else:
            messages.error(request, "Erro ao atualizar o perfil. Verifique os dados.")
    else:
        form = EditProfileForm(instance=user)

    return render(request, 'usuarios/editar_perfil.html', {'form': form})

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