# mensagens/models.py
from django.db import models


class Mensagem(models.Model):
    remetente = models.ForeignKey('usuarios.Usuario', related_name='mensagens_enviadas', on_delete=models.CASCADE)
    destinatario = models.ForeignKey('usuarios.Usuario', related_name='mensagens_recebidas', on_delete=models.CASCADE)
    assunto = models.CharField(max_length=200)
    conteudo = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)
    lida = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.remetente} para {self.destinatario}: {self.assunto}"

class Mensagem(models.Model):
    titulo = models.CharField(max_length=100)
    conteudo = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
    
