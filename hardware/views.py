from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import date, timedelta
from .models import Loja, Componente, HistoricoPreco
from .serializers import LojaSerializer, ComponenteSerializer, HistoricoPrecoSerializer

class LojaViewSet(viewsets.ModelViewSet):
    queryset = Loja.objects.all() 
    serializer_class = LojaSerializer 

class HistoricoPrecoViewSet(viewsets.ModelViewSet):
    queryset = HistoricoPreco.objects.all()
    serializer_class = HistoricoPrecoSerializer

class ComponenteViewSet(viewsets.ModelViewSet):
    queryset = Componente.objects.all()
    serializer_class = ComponenteSerializer

    # 1. Endpoint: Qual loja tem o menor preço atual da peça?
    # Rota: GET /api/componentes/{id}/menor_preco/
    @action(detail=True, methods=['get'])
    def menor_preco(self, request, pk=None):
        componente = self.get_object() # Pega a peça específica pelo ID 
        # Filtra o histórico desta peça e ordena do preço mais baixo para o mais alto
        menor_registro = HistoricoPreco.objects.filter(componente=componente).order_by('preco').first()
            
        if menor_registro:
            serializer = HistoricoPrecoSerializer(menor_registro)
            return Response(serializer.data)    
        return Response({"mensagem": "Ainda não há preços registados para esta peça."}, status=404)

    # 2. Endpoint: Gráfico JSON dos últimos 6 meses (180 dias)
    # Rota: GET /api/componentes/{id}/grafico/
    @action(detail=True, methods=['get'])
    def grafico(self, request, pk=None):
        componente = self.get_object()
        seis_meses_atras = date.today() - timedelta(days=180)
        # Filtra registros desta peça que sejam MAIORES ou IGUAIS a 6 meses atrás
        historico = HistoricoPreco.objects.filter(
            componente=componente,
            data_coleta__gte=seis_meses_atras
        ).order_by('data_coleta')
            
        # Formata a resposta para entregar um JSON limpo
        dados_grafico = [
            {
                "data": registro.data_coleta.strftime("%Y-%m-%d"),
                "preco": float(registro.preco),
                "loja": registro.loja.nome
            }
            for registro in historico
        ]
            
        return Response({
            "componente": componente.nome,
            "total_registos": len(dados_grafico),
            "historico": dados_grafico
        })