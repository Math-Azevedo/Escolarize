# usuarios/templatetags/filtros.py

from django import template

register = template.Library()

@register.filter
def add_class(value, class_name):
    """Adiciona uma classe CSS ao campo do formulário"""
    return value.as_widget(attrs={'class': class_name})


@register.filter
def get_item(dictionary, key):
    """Retorna um item de um dicionário"""
    return dictionary.get(key)

@register.filter
def my_custom_filter(value):
    # lógica do filtro
    return value