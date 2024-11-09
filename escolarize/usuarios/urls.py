# urls.py
from django.urls import path, include
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('home', views.home_view, name='home'),
    path('', views.login_view, name='login'),
    path('aluno/cadastro/', views.cadastrar_aluno, name='cadastro_aluno'),
    path('professor/cadastro/', views.cadastrar_professor, name='cadastro_professor'),
    path('responsavel/cadastro/', views.cadastrar_responsavel, name='cadastro_responsavel'),
    path('logout/', views.logout, name='logout'),
    
]