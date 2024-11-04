# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Mensagem

def lista_mensagens(request):
    mensagens = Mensagem.objects.all().order_by('-data_criacao')  # Ordena pela data, mais recente primeiro
    return render(request, 'mensagens/lista_mensagens.html', {'mensagens': mensagens})

def nova_mensagem(request):
    # Aqui você pode adicionar a lógica para criar uma nova mensagem
    return render(request, 'mensagens/nova_mensagem.html')

def detalhe_mensagem(request, mensagem_id):
    mensagem = get_object_or_404(Mensagem, id=mensagem_id)
    return render(request, 'mensagens/detalhe_mensagem.html', {'mensagem': mensagem})
