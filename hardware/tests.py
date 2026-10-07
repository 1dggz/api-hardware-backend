from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from .models import Loja, Componente, HistoricoPreco


class HardwareAPITests(APITestCase):
    def setUp(self):
        self.usuario = User.objects.create_user('teste', password='senha123')
        self.loja_a = Loja.objects.create(nome='KaBuM!')
        self.loja_b = Loja.objects.create(nome='Pichau')
        self.gpu = Componente.objects.create(nome='RX 6600', categoria='Placa de Vídeo')
        self.hoje = date.today()

    def _preco(self, loja, valor, dias_atras=0):
        return HistoricoPreco.objects.create(
            componente=self.gpu, loja=loja, preco=Decimal(valor),
            data_coleta=self.hoje - timedelta(days=dias_atras),
        )

    # ---- menor_preco ----
    def test_menor_preco_considera_preco_atual_de_cada_loja(self):
        self._preco(self.loja_a, '1000.00', dias_atras=30)  # preço antigo, já superado
        self._preco(self.loja_a, '1500.00')                 # preço atual da KaBuM!
        self._preco(self.loja_b, '1200.00')                 # preço atual da Pichau

        resp = self.client.get(f'/api/componentes/{self.gpu.id}/menor_preco/')

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['loja'], self.loja_b.id)
        self.assertEqual(Decimal(resp.data['preco']), Decimal('1200.00'))

    def test_menor_preco_sem_registros_retorna_404(self):
        resp = self.client.get(f'/api/componentes/{self.gpu.id}/menor_preco/')
        self.assertEqual(resp.status_code, 404)

    # ---- grafico ----
    def test_grafico_ignora_registros_com_mais_de_180_dias(self):
        self._preco(self.loja_a, '1000.00', dias_atras=200)
        self._preco(self.loja_a, '1100.00', dias_atras=10)

        resp = self.client.get(f'/api/componentes/{self.gpu.id}/grafico/')

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['total_registros'], 1)

    # ---- validação ----
    def test_nao_aceita_preco_negativo(self):
        self.client.force_authenticate(self.usuario)
        resp = self.client.post('/api/precos/', {
            'componente': self.gpu.id, 'loja': self.loja_a.id, 'preco': '-10.00',
        })
        self.assertEqual(resp.status_code, 400)

    def test_nao_aceita_preco_duplicado_no_mesmo_dia(self):
        self._preco(self.loja_a, '1000.00')
        self.client.force_authenticate(self.usuario)
        resp = self.client.post('/api/precos/', {
            'componente': self.gpu.id, 'loja': self.loja_a.id,
            'preco': '999.00', 'data_coleta': self.hoje.isoformat(),
        })
        self.assertEqual(resp.status_code, 400)

    # ---- permissão ----
    def test_escrita_exige_autenticacao(self):
        resp = self.client.post('/api/lojas/', {'nome': 'Terabyte'})
        self.assertIn(resp.status_code, (401, 403))

    def test_leitura_e_publica(self):
        resp = self.client.get('/api/lojas/')
        self.assertEqual(resp.status_code, 200)