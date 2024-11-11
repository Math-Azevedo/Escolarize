from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.urls import reverse
from django.contrib.auth import logout as django_logout
from .forms import UsuarioForm, AlunoForm, ProfessorForm, ResponsavelForm
from .models import Usuario, Aluno, Professor, Responsavel

def logout(request):
    django_logout(request)
    return redirect('usuarios:login')

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
        usuario_form = UsuarioForm(request.POST)
        aluno_form = AlunoForm(request.POST)

        if usuario_form.is_valid() and aluno_form.is_valid():
            try:
                # Salvar usuário
                usuario = usuario_form.save(commit=False)
                usuario.tipo_usuario = 'ALUNO'
                usuario.set_password(usuario_form.cleaned_data['password1'])
                usuario.is_responsavel = False
                usuario.is_aluno = True
                usuario.is_professor = False
                usuario.save()

                # Salvar aluno
                aluno = aluno_form.save(commit=False)
                aluno.usuario = usuario
                aluno.save()

                # Mensagem de sucesso
                messages.success(request, 'Aluno cadastrado com sucesso!')
                
                # Limpar formulários após o salvamento (mantendo a página de cadastro aberta)
                usuario_form = UsuarioForm()  # formulário vazio
                aluno_form = AlunoForm()  # formulário vazio

                # Retornar para a mesma página com os formulários vazios
                return render(request, 'usuarios/cadastro_aluno.html', {
                    'usuario_form': usuario_form,
                    'aluno_form': aluno_form
                })
            except Exception as e:
                messages.warning(request, f'Erro ao criar aluno: {str(e)}')
        else:
            messages.warning(request, 'Por favor, corrija os erros abaixo.')
    else:
        usuario_form = UsuarioForm()
        aluno_form = AlunoForm()

    return render(request, 'usuarios/cadastro_aluno.html', {
        'usuario_form': usuario_form,
        'aluno_form': aluno_form
    })


def cadastrar_professor(request):
    if not request.user.is_superuser:
        messages.error(request, 'Você não tem permissão para acessar esta página.')
        return redirect('usuarios:home')
    
    if request.method == 'POST':
        usuario_form = UsuarioForm(request.POST)
        professor_form = ProfessorForm(request.POST)

        if usuario_form.is_valid() and professor_form.is_valid():
            try:
                # Salvar usuário
                usuario = usuario_form.save(commit=False)
                usuario.tipo_usuario = 'PROFESSOR'
                usuario.set_password(usuario_form.cleaned_data['password1'])
                usuario.is_responsavel = False
                usuario.is_aluno = False
                usuario.is_professor = True
                usuario.save()

                # Salvar professor
                professor = professor_form.save(commit=False)
                professor.usuario = usuario
                professor.save()

                # Mensagem de sucesso
                messages.success(request, 'Professor cadastrado com sucesso!')
                
                # Limpar formulários após o salvamento
                usuario_form = UsuarioForm()  # formulário vazio
                professor_form = ProfessorForm()  # formulário vazio

                # Retornar para a mesma página com os formulários vazios
                return render(request, 'usuarios/cadastro_professor.html', {
                    'usuario_form': usuario_form,
                    'professor_form': professor_form
                })
            except Exception as e:
                messages.warning(request, f'Erro ao criar professor: {str(e)}')
        else:
            messages.warning(request, 'Por favor, corrija os erros abaixo.')
    else:
        usuario_form = UsuarioForm()
        professor_form = ProfessorForm()

    return render(request, 'usuarios/cadastro_professor.html', {
        'usuario_form': usuario_form,
        'professor_form': professor_form
    })

def cadastrar_responsavel(request):
    if request.method == 'POST':
        user_form = UsuarioForm(request.POST)
        responsavel_form = ResponsavelForm(request.POST)

        if user_form.is_valid() and responsavel_form.is_valid():
            try:
                with transaction.atomic():
                    # Salvar usuário
                    user = user_form.save(commit=False)
                    user.set_password(user_form.cleaned_data['password1'])
                    user.is_responsavel = True
                    user.is_aluno = False
                    user.is_professor = False
                    user.save()

                    # Salvar responsável
                    responsavel = responsavel_form.save(commit=False)
                    responsavel.usuario = user
                    responsavel.save()

                    # Fazer login do usuário
                    login(request, user)
                    messages.success(request, 'Cadastro realizado com sucesso!')
                    
                    # Limpar formulários após o salvamento
                    user_form = UsuarioForm()  # formulário vazio
                    responsavel_form = ResponsavelForm()  # formulário vazio

                    # Retornar para a mesma página com os formulários vazios
                    return render(request, 'usuarios/cadastro_responsavel.html', {
                        'user_form': user_form,
                        'responsavel_form': responsavel_form
                    })
            except Exception as e:
                messages.error(request, f'Ocorreu um erro ao realizar o cadastro: {str(e)}')
        else:
            messages.warning(request, 'Por favor, corrija os erros abaixo.')
    else:
        user_form = UsuarioForm()
        responsavel_form = ResponsavelForm()

    return render(request, 'usuarios/cadastro_responsavel.html', {
        'user_form': user_form,
        'responsavel_form': responsavel_form
    })
