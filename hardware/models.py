from django.db import models
from datetime import date
from decimal import Decimal
from django.core.validators import MinValueValidator

# Classe Loja
class Loja(models.Model):
    nome = models.CharField(max_length=100)
    site = models.URLField(blank=True, null=True)
    def __str__(self):
        return self.nome

# Classe Hardwares
class Componente(models.Model):
    nome = models.CharField(max_length=150)
    categoria = models.CharField(max_length=100)
    def __str__(self):
        return self.nome

# Classe Registro de Preços
class HistoricoPreco(models.Model):
    componente = models.ForeignKey(Componente, on_delete=models.PROTECT)
    loja = models.ForeignKey(Loja, on_delete=models.PROTECT)
    preco = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(Decimal('0.01'))])
    data_coleta = models.DateField(default=date.today)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['componente', 'loja', 'data_coleta'],
                name='preco_unico_por_peca_loja_dia',
            )
        ]
