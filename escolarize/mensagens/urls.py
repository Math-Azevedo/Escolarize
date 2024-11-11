# mensagens/urls.py
from django.urls import path
from . import views

app_name = 'mensagens'

urlpatterns = [
    path('lista_mensagens', views.lista_mensagens, name='lista_mensagens'),
    path('nova/', views.nova_mensagem, name='nova_mensagem'),
    path('<int:mensagem_id>/', views.detalhe_mensagem, name='detalhe_mensagem'),
]