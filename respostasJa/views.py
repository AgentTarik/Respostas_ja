from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
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



def register_view(request):
    if request.method == "POST":
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
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

def criar_formulario_view(request):
    if request.user.quantidade_formularios_respondidos < 5:
        messages.error(request, "Você precisa responder pelo menos 5 formulários antes de criar um.")
        return redirect("listar-formularios")

    if request.method == "POST":
        titulo = request.POST.get("titulo")
        formulario = Formulario.objects.create(
            titulo=titulo,
            usuario=request.user
        )

        perguntas_data = request.POST.getlist("perguntas[texto]")
        tipos_data = request.POST.getlist("perguntas[tipo]")
        opcoes_data = request.POST.getlist("perguntas[opcoes][]")

        for i, pergunta_texto in enumerate(perguntas_data):
            tipo = tipos_data[i]
            tipo_de_pergunta = TipoDePergunta.objects.get(tipo=tipo)

            # Cria a pergunta
            pergunta = Pergunta.objects.create(
                pergunta=pergunta_texto,
                formulario=formulario,
                tipo_de_pergunta=tipo_de_pergunta
            )

            # Salva as opções, se for checkbox ou múltipla escolha
            if tipo in ["checkbox", "multipla_escolha"]:
                opcoes = request.POST.getlist(f"perguntas[{i}][opcoes][]")
                if opcoes:  # Certifique-se de que as opções não estão vazias
                    pergunta.possiveisRespostas = opcoes
                    pergunta.save()


        request.user.quantidade_formularios_respondidos -= 5
        request.user.save()

        return redirect("meus_formularios")  # Redirecionar após salvar o formulário

    return render(request, "criar_formulario.html")



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
    formulario = get_object_or_404(Formulario, id=formulario_id)
    perguntas = formulario.perguntas.all()

    if request.method == "POST":
        errors = []

        for pergunta in perguntas:
            if pergunta.tipo_de_pergunta.tipo == "textbox":
                resposta = request.POST.get(f"resposta_{pergunta.id}")
                if not resposta or not resposta.strip():
                    errors.append(f"A pergunta '{pergunta.pergunta}' não foi respondida.")

            elif pergunta.tipo_de_pergunta.tipo == "multipla_escolha":
                resposta = request.POST.get(f"resposta_{pergunta.id}")
                if not resposta:
                    errors.append(f"A pergunta '{pergunta.pergunta}' não foi respondida.")

        if errors:
            return render(request, "responder_formulario.html", {
                "formulario": formulario,
                "perguntas": perguntas,
                "errors": errors
            })
        

        for pergunta in perguntas:
            if pergunta.tipo_de_pergunta.tipo == "textbox":
                # Salvar resposta de texto
                resposta_texto = request.POST.get(f"resposta_{pergunta.id}")
                if resposta_texto:
                    RespostaCampo.objects.create(texto=resposta_texto, pergunta=pergunta)

            elif pergunta.tipo_de_pergunta.tipo == "multipla_escolha":
                # Salvar resposta de múltipla escolha
                resposta_opcao = request.POST.get(f"resposta_{pergunta.id}")
                if resposta_opcao:
                    RespostaCampo.objects.create(texto=resposta_opcao, pergunta=pergunta)

            elif pergunta.tipo_de_pergunta.tipo == "checkbox":
                # Salvar todas as respostas de checkbox selecionadas
                resposta_opcoes = request.POST.getlist(f"resposta_{pergunta.id}[]") 
                for resposta_opcao in resposta_opcoes:
                    RespostaCampo.objects.create(texto=resposta_opcao, pergunta=pergunta)

        if request.user.is_authenticated and formulario.usuario != request.user :
            usuario = request.user
            usuario.quantidade_formularios_respondidos += 1
            usuario.save()

        return redirect("agradecimento")  # Redirecionar para a página de agradecimento após salvar as respostas

    return render(request, "responder_formulario.html", {
        "formulario": formulario,
        "perguntas": perguntas
    })


@login_required
def meus_formularios_view(request):
    formularios = Formulario.objects.filter(usuario=request.user)
    return render(request, "meus_formularios.html", {"formularios": formularios})


@login_required
def toggle_status_view(request, formulario_id):
    formulario = get_object_or_404(Formulario, id=formulario_id, usuario=request.user)
    if formulario.status == "ativo":
        formulario.status = "inativo"
    else:
        formulario.status = "ativo"
    formulario.save()
    return redirect("meus_formularios")


