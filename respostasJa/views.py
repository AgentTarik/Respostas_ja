from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UsuarioCreationForm

# Página de login
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home") 
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
            return redirect("home")  
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
