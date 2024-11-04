# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .forms import UsuarioForm, AlunoForm, ProfessorForm, ResponsavelForm
from .models import Usuario, Aluno, Professor, Responsavel
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.urls import reverse


def logout(request):
    return render(request, 'usuarios/login.html')

def home_view(request):
    return render(request, 'core/home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'core/home.html')
        else:
            messages.error(request, 'Credenciais inválidas')
    return render(request, 'usuarios/login.html')

def cadastrar_aluno(request):
    if request.method == 'POST':
        try:
            # Criar formulário de usuário com os dados do POST
            usuario_form = UsuarioForm(request.POST)
            aluno_form = AlunoForm(request.POST)

            if usuario_form.is_valid() and aluno_form.is_valid():
                # Salvar usuário
                usuario = usuario_form.save(commit=False)
                usuario.tipo_usuario = 'ALUNO'
                usuario.set_password(usuario_form.cleaned_data['password1'])
                usuario.save()

                # Salvar aluno
                aluno = aluno_form.save(commit=False)
                aluno.usuario = usuario
                aluno.save()

                messages.success(request, 'Aluno cadastrado com sucesso!')
                return redirect('login')
            else:
                messages.warning(request, 'Por favor, corrija os erros abaixo.')
        except Exception as e:
            messages.warning(request, f'Erro ao criar usuário: {str(e)}')
    else:
        usuario_form = UsuarioForm()
        aluno_form = AlunoForm()

    context = {
        'usuario_form': usuario_form,
        'aluno_form': aluno_form
    }
    return render(request, 'cadastro_aluno.html', context)

def cadastrar_professor(request):
    if not request.user.is_superuser:
        messages.error(request, 'Você não tem permissão para acessar esta página.')
        return redirect('home')
    
    if request.method == 'POST':
        try:
            usuario_form = UsuarioForm(request.POST)
            professor_form = ProfessorForm(request.POST)

            if usuario_form.is_valid() and professor_form.is_valid():
                usuario = usuario_form.save(commit=False)
                usuario.tipo_usuario = 'PROFESSOR'
                usuario.set_password(usuario_form.cleaned_data['password1'])
                usuario.save()

                professor = professor_form.save(commit=False)
                professor.usuario = usuario
                professor.save()
                professor_form.save_m2m()

                messages.success(request, 'Professor cadastrado com sucesso!')
                return redirect('home')
            else:
                messages.warning(request, 'Por favor, corrija os erros abaixo.')
        except Exception as e:
            messages.warning(request, f'Erro ao criar professor: {str(e)}')
    else:
        usuario_form = UsuarioForm()
        professor_form = ProfessorForm()

    context = {
        'usuario_form': usuario_form,
        'professor_form': professor_form
    }
    return render(request, 'usuarios/cadastro_professor.html', context)

def cadastrar_responsavel(request):
    if request.method == 'POST':
        user_form = UsuarioForm(request.POST)
        responsavel_form = ResponsavelForm(request.POST)

        if user_form.is_valid() and responsavel_form.is_valid():
            try:
                with transaction.atomic():
                    # Cria o usuário
                    user = user_form.save()
                    
                    # Cria o perfil do responsável
                    responsavel = responsavel_form.save(commit=False)
                    responsavel.user = user
                    responsavel.save()

                    # Faz login do usuário
                    login(request, user)
                    messages.success(request, 'Cadastro realizado com sucesso!')
                    return redirect('home')  # Substitua 'home' pela sua URL de redirecionamento
            
            except Exception as e:
                messages.error(request, 'Ocorreu um erro ao realizar o cadastro.')
                print(f"Erro no cadastro: {str(e)}")
    else:
        user_form = UsuarioForm()
        responsavel_form = ResponsavelForm()
    
    return render(request, 'usuarios/cadastro_responsavel.html', {
        'user_form': user_form,
        'responsavel_form': responsavel_form
    })