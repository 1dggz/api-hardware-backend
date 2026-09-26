from django.db import models
from datetime import date

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
    componente = models.ForeignKey(Componente, on_delete=models.CASCADE)
    loja = models.ForeignKey(Loja, on_delete=models.CASCADE)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    data_coleta = models.DateField(default=date.today)
    def __str__(self):
        return f"{self.componente.nome} na {self.loja.nome} por R$ {self.preco}"
