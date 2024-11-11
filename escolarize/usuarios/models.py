# usuarios/models.py
from django.contrib.auth.models import AbstractUser, User
from django.db import models
from notas.models import Materia, Serie
from django.conf import settings
from django.utils import timezone

class Usuario(AbstractUser):
    TIPOS_USUARIO = (
        ('SUPERUSER', 'Superusuário'),
        ('PROFESSOR', 'Professor'),
        ('ALUNO', 'Aluno'),
        ('RESPONSAVEL', 'Responsável'),
    )
    tipo_usuario = models.CharField(max_length=20, choices=TIPOS_USUARIO)
    telefone = models.CharField(max_length=15, blank=True)
    
    # Campos booleanos para indicar o tipo de usuário
    is_responsavel = models.BooleanField(default=False)
    is_aluno = models.BooleanField(default=False)
    is_professor = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Professor(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    identificador = models.CharField(max_length=20, unique=True)
    formacao = models.CharField(max_length=100)
    series = models.ManyToManyField(Serie, related_name="professores")
    materias = models.ManyToManyField(Materia, related_name="professores")
    password = models.CharField(max_length=128,default='senha123') 

    def __str__(self):
        return self.usuario.get_full_name()

class Responsavel(models.Model):
    # Altere para usar o modelo de usuário configurado em settings.py
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    cpf = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=15)
    endereco = models.CharField(max_length=200)
    data_nascimento = models.DateField()
    
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro')
    ]
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.usuario.first_name} {self.usuario.last_name}"

    class Meta:
        verbose_name = 'Responsável'
        verbose_name_plural = 'Responsáveis'

class Aluno(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    matricula = models.CharField(max_length=20, unique=True)
    data_nascimento = models.DateField()
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE, related_name="alunos")
    responsavel = models.ForeignKey(Responsavel, on_delete=models.CASCADE, related_name="alunos")
    password = models.CharField(max_length=128, default='senha123') 

    def __str__(self):
        return self.usuario.get_full_name()