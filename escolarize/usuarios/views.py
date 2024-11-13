#usuaris/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.urls import reverse
from notas.models import Serie
from .forms import AlunoForm, PaiMaeForm, UsuarioForm, AlunoUsuarioForm, ProfessorForm, ResponsavelForm
from .models import PaiMae, Usuario, Aluno, Professor, Responsavel
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



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
        aluno_form = AlunoUsuarioForm(request.POST)
        
        if aluno_form.is_valid():
            aluno = aluno_form.save(commit=False)
            pai_mae = aluno_form.cleaned_data['pai_mae']
            aluno.pai_mae = pai_mae
            aluno.save()
            return redirect('sucesso')  # Redirecionar para a página de sucesso
        else:
            return render(request, 'usuarios/cadastro_aluno.html', {'form': aluno_form})
    else:
        usuario_form = UsuarioForm()
        aluno_form = AlunoUsuarioForm()

    return render(request, 'usuarios/cadastro_aluno.html', {'usuario_form': usuario_form, 'form': aluno_form})

def cadastrar_aluno(request):
    if request.method == 'POST':
        aluno_form = AlunoForm(request.POST)
        if aluno_form.is_valid():
            aluno = aluno_form.save()  # Salva o aluno
            return redirect('sucesso')  # Redireciona para uma página de sucesso
    else:
        aluno_form = AlunoForm()

    return render(request, 'cadastro_aluno.html', {'aluno_form': aluno_form})

def cadastrar_pai_mae(request):
    if request.method == 'POST':
        pai_mae_form = PaiMaeForm(request.POST)
        if pai_mae_form.is_valid():
            pai_mae = pai_mae_form.save()  # Salva o pai/mãe
            return redirect('sucesso')
    else:
        pai_mae_form = PaiMaeForm()

    return render(request, 'cadastro_pai_mae.html', {'pai_mae_form': pai_mae_form})

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
        usuario_form = UsuarioForm(request.POST)
        responsavel_form = ResponsavelForm(request.POST)

        
        if usuario_form.is_valid() and responsavel_form.is_valid():
            print('entrou')
            usuario = usuario_form.save(commit=False)
            
            usuario.save()
            responsavel = responsavel_form.save(commit=False)
            responsavel.user = usuario  # Associa o usuário ao responsável
            responsavel.save()  # Salva o responsável
            
            # Redireciona após salvar
            return redirect('home')  
        else:
            # Caso o formulário não seja válido, renderiza novamente com erros
            return render(request, 'usuarios/cadastro_responsavel.html', {
                'usuario_form': usuario_form,
                'responsavel_form': responsavel_form
            })
    else:
        # Caso GET
        usuario_form = UsuarioForm()
        responsavel_form = ResponsavelForm()

    return render(request, 'usuarios/cadastro_responsavel.html', {
        'usuario_form': usuario_form,
        'responsavel_form': responsavel_form
    })
