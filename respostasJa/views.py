from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import Formulario, Pergunta, TipoDePergunta, RespostaCampo

from .forms import UsuarioCreationForm

# Página de login
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("listar-formularios") 
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


# Página de registro
def register_view(request):
    if request.method == "POST":
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  
            login(request, user)  # Faz login automaticamente
            return redirect("listar-formularios")  
    else:
        form = UsuarioCreationForm()
    return render(request, "register.html", {"form": form})


# Página inicial acessível apenas para usuários logados
@login_required
def home_view(request):
    return render(request, "home.html")


def logout_view(request):
    logout(request)
    return redirect("login")  # Redireciona para a página de login após o logout


def sobre_nos_view(request):
    return render(request, "sobre.html")


@login_required
def criar_formulario_view(request):
    if request.method == "POST":
        # Cria o formulário
        titulo = request.POST.get("titulo")
        usuario = request.user
        formulario = Formulario.objects.create(titulo=titulo, usuario=usuario)

        # Processa as perguntas associadas
        perguntas = request.POST.getlist("pergunta[]")
        tipos = request.POST.getlist("tipo_de_pergunta[]")

        for pergunta_texto, tipo in zip(perguntas, tipos):
            tipo_de_pergunta = TipoDePergunta.objects.get(tipo=tipo)
            Pergunta.objects.create(
                pergunta=pergunta_texto,
                formulario=formulario,
                tipo_de_pergunta=tipo_de_pergunta
            )

        return redirect("listar-formularios")  # Redireciona após salvar

    # Recupera os tipos de perguntas disponíveis
    tipos_de_perguntas = TipoDePergunta.objects.all()
    return render(request, "criar_formulario.html", {"tipos_de_perguntas": tipos_de_perguntas})


@login_required
def listar_formularios(request):
    if request.user.is_authenticated:  # Verifica se o usuário está logado
        # Busca os formulários ativos associados ao usuário logado
        formularios = Formulario.objects.all()
    else:
        formularios = [] 
    return render(request, "formularios.html", {"formularios": formularios})


@login_required
def meu_perfil_view(request):
    usuario = request.user
    return render(request, "meu_perfil.html", {"usuario": usuario})


def responder_formulario_view(request, formulario_id):
    # Busca o formulário pelo ID
    formulario = get_object_or_404(Formulario, id=formulario_id)
    
    if request.method == "POST":
        # Processa as respostas enviadas
        respostas = request.POST.getlist("respostas[]")
        perguntas = Pergunta.objects.filter(formulario=formulario)
        
        for pergunta, resposta_texto in zip(perguntas, respostas):
            RespostaCampo.objects.create(
                texto=resposta_texto,
                pergunta=pergunta
            )
        
        # Redireciona para uma página de confirmação ou de agradecimento
        return redirect("agradecimento")
    
    # Recupera todas as perguntas do formulário
    perguntas = Pergunta.objects.filter(formulario=formulario)
    return render(request, "responder_formulario.html", {"formulario": formulario, "perguntas": perguntas})


