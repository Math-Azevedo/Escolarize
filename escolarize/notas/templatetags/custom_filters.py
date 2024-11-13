# notas/templatetags/custom_filters.py
from django import template
from django.apps import apps

register = template.Library()

# Obtém os modelos necessários
AlunoMateria = apps.get_model('notas', 'AlunoMateria')

@register.filter
def get_nota(aluno, materia):
    """
    Retorna a nota do aluno em uma determinada matéria.
    Uso no template: {{ aluno|get_nota:materia }}
    """
    try:
        aluno_materia = AlunoMateria.objects.get(
            aluno=aluno,
            materia=materia,
            # Você pode adicionar mais filtros aqui se necessário
            # como ano_letivo e periodo
        )
        return aluno_materia.nota if aluno_materia.nota else '-'
    except AlunoMateria.DoesNotExist:
        return '-'

@register.filter
def get_frequencia(aluno, materia):
    """
    Retorna a frequência do aluno em uma determinada matéria.
    Uso no template: {{ aluno|get_frequencia:materia }}
    """
    try:
        aluno_materia = AlunoMateria.objects.get(
            aluno=aluno,
            materia=materia,
            # Você pode adicionar mais filtros aqui se necessário
            # como ano_letivo e periodo
        )
        return f"{aluno_materia.frequencia}%" if aluno_materia.frequencia else '-'
    except AlunoMateria.DoesNotExist:
        return '-'