# API de Monitoramento e Inventário de Hardware 🖥️

Uma API REST desenvolvida em Python e Django para catalogar componentes de hardware e registrar o histórico de preços em diferentes lojas. Projeto acadêmico desenvolvido para a disciplina de Web Back-end.

## 🛠️ Tecnologias Utilizadas
* **Python**
* **Django**
* **Django REST Framework (DRF)**
* **SQLite** (Banco de dados nativo)

## ⚙️ Como executar o projeto localmente

1. **Clonar o repositório**

   ```bash
   git clone https://github.com/1dggz/api-hardware-backend.git
   cd api-hardware-backend

3. **Criar e ativar o ambiente virtual**

    ```bash
   python -m venv venv

   # No Windows (PowerShell):
   venv\Scripts\activate

   # No Linux/Mac:
   source venv/bin/activate

4. **Instalar as dependências**

    ```bash
   pip install django djangorestframework

5. **Executar as migrações do banco de dados**

    ```bash
   python manage.py migrate

7. **Iniciar o servidor local**

   ```bash
   python manage.py runserver

## 🔗 Endpoints e Funcionalidades

Abaixo estão as rotas disponíveis no sistema. As rotas de listagem suportam os métodos nativos de CRUD: `GET` (Ler), `POST` (Criar), `PUT` (Atualizar) e `DELETE` (Apagar).

## 🏪 Lojas

* **Listar todas as lojas: `GET` /api/lojas/**
* **Detalhes de uma loja específica: `GET` /api/lojas/{id}/**
* **Exemplo de payload para criação (`POST`):**
  
   ```bash
   {
   "nome": "KaBuM!",
   "site": "[https://www.kabum.com.br](https://www.kabum.com.br)"
   }

## 💻 Componentes

* **Listar todas as peças: `GET` /api/componentes/**
* **Detalhes de uma peça: `GET` /api/componentes/{id}/**
* **Exemplo de payload para criação (`POST`):**
  
   ```bash
   {
   "nome": "Placa de Vídeo RX 6600",
   "categoria": "Placa de Vídeo"  
   }

## 📈 Histórico de Preços e Regras de Negócio

Além do CRUD padrão (`GET /api/precos/`), a API conta com rotas customizadas para extração de análises focadas na decisão de compra:

* **Menor preço atual de uma peça:** `GET /api/componentes/{id}/menor_preco/`  
  > Retorna o registro histórico com o valor monetário mais baixo já cadastrado para aquele componente específico, auxiliando na identificação da melhor loja para compra.

* **Dados para gráfico de variação (Últimos 6 meses):** `GET /api/componentes/{id}/grafico/`  
  > Retorna um JSON estruturado contendo a flutuação de preço da peça nos últimos 180 dias.
