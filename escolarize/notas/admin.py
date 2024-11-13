# notas/admin.py
from django.contrib import admin
from .models import AlunoMateria

@admin.register(AlunoMateria)
class AlunoMateriaAdmin(admin.ModelAdmin):
    list_display = ['aluno', 'materia', 'ano_letivo', 'periodo', 'nota', 'frequencia']
    list_filter = ['ano_letivo', 'periodo', 'materia']
    search_fields = ['aluno__usuario__first_name', 'aluno__usuario__last_name', 'materia__nome']
