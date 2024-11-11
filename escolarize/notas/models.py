# notas/models.py
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Serie(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.nome

class Materia(models.Model):
    nome = models.CharField(max_length=100)
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE, related_name='materias')

    def __str__(self):
        return self.nome
    
class Disciplina(models.Model):
    nome = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nome

class Nota(models.Model):
    aluno = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=4, decimal_places=2)
    data = models.DateField(auto_now_add=True)
    bimestre = models.IntegerField(choices=[
        (1, '1º Bimestre'),
        (2, '2º Bimestre'),
        (3, '3º Bimestre'),
        (4, '4º Bimestre')
    ])
    ano = models.IntegerField()
    
    class Meta:
        ordering = ['-ano', 'disciplina', 'bimestre']
    
    def __str__(self):
        return f"{self.aluno.username} - {self.disciplina.nome} - {self.bimestre}º Bimestre {self.ano}"

        return f"{self.aluno} - {self.materia} - {self.bimestre}º Bim: {self.nota}"
