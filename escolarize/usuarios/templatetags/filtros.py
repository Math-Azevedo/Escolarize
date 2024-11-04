# usuarios/templatetags/filtros.py

from django import template

register = template.Library()

@register.filter
def add_class(value, class_name):
    """Adiciona uma classe CSS ao campo do formulário"""
    return value.as_widget(attrs={'class': class_name})
