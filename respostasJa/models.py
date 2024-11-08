from django.db import models

class Usuario(models.Model):
    idUsuario = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=128)

    def __str__(self):
        return self.idUsuario

class Formulario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='formularios')
    idFormulario = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=200)

    def __str__(self):
        return self.titulo

class Campo(models.Model):
    formulario = models.ForeignKey(Formulario, on_delete=models.CASCADE, related_name='campos')
    tipo = models.CharField(max_length=50)
    pergunta = models.CharField(max_length=255)godels.CASCADE, related_name='respostas')
    campo = models.ForeignKey(Campo, on_delete=models.CASCADE, related_name='respostas')
    idResposta = models.AutoField(primary_key=True)
    conteudo = models.TextField()

    def __str__(self):
        return f"Resposta {self.idResposta} para {self.campo.pergunta}"