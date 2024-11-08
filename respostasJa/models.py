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
    pergunta = models.CharField(max_length=255)

    def __str__(self):
        return f"{Formulario.idFormulario} {self.campo.pergunta}"

class RespostaFormulario(models.Model):
    formulario = models.ForeignKey(Formulario, on_delete=models.CASCADE, related_name='respostas_formulario')
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='respostas_formulario')
    data_resposta = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Respostas para {self.formulario.titulo} por {self.usuario.idUsuario if self.usuario else 'Usuário Anônimo'}"

class RespostaCampo(models.Model):
    resposta_formulario = models.ForeignKey(RespostaFormulario, on_delete=models.CASCADE, related_name='respostas_campos')
    campo = models.ForeignKey(Campo, on_delete=models.CASCADE, related_name='respostas')
    conteudo = models.TextField()

    def __str__(self):
        return f"Resposta para '{self.campo.pergunta}': {self.conteudo}"
