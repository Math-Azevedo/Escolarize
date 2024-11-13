# mensagens/models.py
from django.db import models
from usuarios.models import PaiMae, Professor

class Mensagem(models.Model):
    remetente = models.ForeignKey(PaiMae, on_delete=models.CASCADE, related_name='mensagens_enviadas')
    destinatario = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='mensagens_recebidas')
    conteudo = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)  # altere para 'data_envio'
    assunto = models.CharField(max_length=100, default='Assunto padrão')  # com valor padrão


    def __str__(self):
        return f"{self.remetente} para {self.destinatario}: {self.assunto}"
