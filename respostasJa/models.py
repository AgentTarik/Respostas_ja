from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    quantidade_formularios_respondidos = models.IntegerField(default=0)

    def __str__(self):
        return self.username

class Formulario(models.Model):
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
    ]
    titulo = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ativo')
    quantidade_formularios_respondidos = models.IntegerField(default=0)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='formularios')

    def __str__(self):
        return self.titulo


class TipoDePergunta(models.Model):
    TIPO_CHOICES = [
        ('textbox', 'TextBox'),
        ('checkbox', 'CheckBox'),
        ('multipla_escolha', 'Múltipla Escolha'),
    ]
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)

    def __str__(self):
        return self.get_tipo_display()


class Pergunta(models.Model):
    pergunta = models.TextField()
    formulario = models.ForeignKey(Formulario, on_delete=models.CASCADE, related_name='perguntas')
    tipo_de_pergunta = models.ForeignKey(TipoDePergunta, on_delete=models.CASCADE, related_name='perguntas')

    possiveisRespostas = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.pergunta


class RespostaCampo(models.Model):
    texto = models.TextField()
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE, related_name='respostas')

    def __str__(self):
        return self.texto[:50]