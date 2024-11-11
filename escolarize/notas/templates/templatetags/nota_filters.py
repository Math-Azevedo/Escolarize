# notas/templatetags/nota_filters.py
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key_tuple):
    aluno_id, disciplina_id = key_tuple
    return dictionary.get((aluno_id, disciplina_id))

@register.filter
def get_nota1(nota):
    return nota.nota1 if nota else 0

@register.filter
def get_nota2(nota):
    return nota.nota2 if nota else 0

@register.filter
def get_nota3(nota):
    return nota.nota3 if nota else 0

@register.filter
def get_nota4(nota):
    return nota.nota4 if nota else 0
