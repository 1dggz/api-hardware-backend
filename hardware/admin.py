from django.contrib import admin
from .models import Loja, Componente, HistoricoPreco

@admin.register(Loja)
class LojaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'site')
    search_fields = ('nome',)

@admin.register(Componente)
class ComponenteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria')
    list_filter = ('categoria',)
    search_fields = ('nome',)

@admin.register(HistoricoPreco)
class HistoricoPrecoAdmin(admin.ModelAdmin):
    list_display = ('componente', 'loja', 'preco', 'data_coleta')
    list_filter = ('loja', 'data_coleta')
    search_fields = ('componente__nome',)