from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Formulario, TipoDePergunta, Pergunta, RespostaCampo

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('quantidade_formularios_respondidos',)}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'quantidade_formularios_respondidos')


@admin.register(Formulario)
class FormularioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'status', 'quantidade_formularios_respondidos', 'usuario')
    list_filter = ('status',)
    search_fields = ('titulo', 'usuario__username')
    autocomplete_fields = ('usuario',)


@admin.register(TipoDePergunta)
class TipoDePerguntaAdmin(admin.ModelAdmin):
    list_display = ('tipo',)
    search_fields = ('tipo',)


@admin.register(Pergunta)
class PerguntaAdmin(admin.ModelAdmin):
    list_display = ('pergunta', 'formulario', 'tipo_de_pergunta')
    search_fields = ('pergunta', 'formulario__titulo')
    autocomplete_fields = ('formulario', 'tipo_de_pergunta')


@admin.register(RespostaCampo)
class RespostaCampoAdmin(admin.ModelAdmin):
    list_display = ('texto', 'pergunta')
    search_fields = ('texto', 'pergunta__pergunta')
    autocomplete_fields = ('pergunta',)
