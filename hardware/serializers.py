from rest_framework import serializers
from .models import Loja, Componente, HistoricoPreco


class LojaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loja
        fields = '__all__' 

class ComponenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Componente
        fields = '__all__'

class HistoricoPrecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricoPreco
        fields = '__all__'