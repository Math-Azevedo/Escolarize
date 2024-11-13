# notas/models.py
from django.apps import apps
from django.db import models


class Serie(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome

class Materia(models.Model):
    nome = models.CharField(max_length=100)
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE, related_name='materias')

    def __str__(self):
        return self.nome

class AlunoMateria(models.Model):
    aluno = models.ForeignKey('usuarios.Aluno', on_delete=models.CASCADE, related_name='materias_cursadas')
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='alunos_matriculados')
    ano_letivo = models.IntegerField()
    periodo = models.IntegerField(choices=[(1, '1º Bimestre'), (2, '2º Bimestre'), (3, '3º Bimestre'), (4, '4º Bimestre')])
    nota = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    frequencia = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = ['aluno', 'materia', 'ano_letivo', 'periodo']

    @property
    def media(self):
        notas = [self.nota_1bimestre, self.nota_2bimestre, self.nota_3bimestre, self.nota_4bimestre]
        notas_validas = [nota for nota in notas if nota is not None]
        if notas_validas:
            return sum(notas_validas) / len(notas_validas)
        return 0  # Ou outro valor padrão se todas as notas forem None

    def __str__(self):
        return f"{self.aluno} - {self.materia} ({self.ano_letivo}/{self.periodo}º Bimestre)"


class Nota(models.Model):
    aluno = models.ForeignKey('usuarios.Aluno', on_delete=models.CASCADE)  # Referência como string
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    nota_1bimestre = models.FloatField(null=True, blank=True)
    nota_2bimestre = models.FloatField(null=True, blank=True)
    nota_3bimestre = models.FloatField(null=True, blank=True)
    nota_4bimestre = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Nota de {self.aluno} para {self.materia}"

    def get_aluno(self):
        from usuarios.models import Aluno  # Importação tardia
        return Aluno.objects.get(id=self.aluno.id)

class Disciplina(models.Model):
    nome = models.CharField(max_length=100)
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE, related_name='disciplina')

    def __str__(self):
        return self.nome

class NotaSerie(models.Model):
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE)
    # outros campos

