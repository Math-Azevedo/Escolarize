# notas/urls.py
from django.urls import path
from . import views

app_name = 'notas'

urlpatterns = [
    path('series/', views.lista_series, name='lista_series'),
    path('series/<int:serie_id>/alunos/', views.alunos_serie, name='alunos_serie'),
    path('historico/', views.historico, name='historico'),
    path('series/<int:serie_id>/lancar-notas/', views.lancar_notas, name='lancar_notas'),
]