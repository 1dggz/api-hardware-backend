from django.contrib import admin
from .models import Loja, Componente, HistoricoPreco

admin.site.register(Loja)
admin.site.register(Componente)
admin.site.register(HistoricoPreco)