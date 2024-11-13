# usuarios/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from notas.models import Materia, Serie
from django.utils import timezone
from django.apps import apps

class Usuario(AbstractUser):
    is_professor = models.BooleanField(default=False)
    is_aluno = models.BooleanField(default=False)
    is_responsavel = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username


class Professor(models.Model):
    nome = models.CharField(max_length=100)
    materias = models.ManyToManyField(Materia)  # Exemplo, se Materia for outro modelo

    identificador = models.CharField(max_length=50)

    series = models.CharField(max_length=50)

    formacao = models.CharField(max_length=100)
    def __str__(self):

        return self.nome

class Aluno(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    identificador = models.CharField(max_length=10)
    nome = models.CharField(max_length=100)
    idade = models.IntegerField()
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE)
    materias = models.ManyToManyField(Materia, related_name='alunos', blank=True)
    professores = models.ManyToManyField(Professor)
    pai_mae = models.ForeignKey('PaiMae', on_delete=models.CASCADE, related_name='alunos', null=False)
    is_pai = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Aluno"
        verbose_name_plural = "Alunos"
        ordering = ['nome']  # Opcional, para definir a ordem padrão
    
    def __str__(self):
        return self.nome



class Responsavel(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='responsaveis')  # Corrigido aqui
    identificador = models.CharField(max_length=9999)
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField(null=True, blank=True)
    cpf = models.CharField(max_length=11, unique=True, null=True, blank=True)
    sexo = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Feminino')], null=True, blank=True)
    endereco = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nome
    

class PaiMae(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    identificador = models.CharField(max_length=9999)
    nome = models.CharField(max_length=100)
    is_pai = models.BooleanField(default=True)

    def __str__(self):
        return self.nome




