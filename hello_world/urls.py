"""
URL configuration for hello_world project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from hello_world.core import views as core_views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from respostasJa import views
from django.shortcuts import render



urlpatterns = [
    path("", views.sobre_nos_view),
    path("admin/", admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("home/", views.home_view, name="home"),
    path("logout/", views.logout_view, name="logout"),
    path("sobre-nos/", views.sobre_nos_view, name="sobre-nos"),
    path("formularios/", views.listar_formularios, name="listar-formularios"),
    path("meu-perfil/", views.meu_perfil_view, name="meu-perfil"),
    path("criar-formulario/", views.criar_formulario_view, name="criar-formulario"),
    path("formulario/<int:formulario_id>/", views.responder_formulario_view, name="responder-formulario"),
    path("agradecimento/", lambda request: render(request, "agradecimento.html"), name="agradecimento"),
    path("meus-formularios/", views.meus_formularios_view, name="meus_formularios"),
    path("toggle-status/<int:formulario_id>/", views.toggle_status_view, name="toggle_status"),
   path('visualizar-respostas/<int:formulario_id>/', views.visualizar_respostas, name='visualizar_respostas'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
