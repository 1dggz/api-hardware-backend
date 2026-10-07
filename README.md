# API de Monitoramento e Inventário de Hardware 🖥️

API REST desenvolvida em Python e Django para catalogar componentes de hardware e registrar o histórico de preços em diferentes lojas, ajudando a identificar a melhor hora e o melhor lugar para comprar uma peça.

Projeto acadêmico desenvolvido para a disciplina de Web Back-end.

## 📋 Sumário

- [Tecnologias utilizadas](#️-tecnologias-utilizadas)
- [Como executar o projeto localmente](#️-como-executar-o-projeto-localmente)
- [Autenticação e permissões](#-autenticação-e-permissões)
- [Endpoints](#-endpoints)
- [Regras de negócio e validações](#-regras-de-negócio-e-validações)
- [Testes automatizados](#-testes-automatizados)
- [Estrutura do projeto](#-estrutura-do-projeto)
- [Variáveis de ambiente](#-variáveis-de-ambiente)

## 🛠️ Tecnologias utilizadas

- **Python** 3.12 ou superior
- **Django**
- **Django REST Framework (DRF)**
- **SQLite** (banco de dados nativo do Django)

## ⚙️ Como executar o projeto localmente

1. **Clonar o repositório**

   ```bash
   git clone https://github.com/1dggz/api-hardware-backend.git
   cd api-hardware-backend
   ```

2. **Criar e ativar o ambiente virtual**

   ```bash
   python -m venv venv

   # No Windows (PowerShell):
   venv\Scripts\activate

   # No Linux/Mac:
   source venv/bin/activate
   ```

3. **Instalar as dependências**

   ```bash
   pip install -r requirements.txt
   ```

4. **Criar o banco de dados (aplicar as migrações)**

   ```bash
   python manage.py migrate
   ```

5. **Criar um usuário administrador** (necessário para criar, editar e apagar dados pela API)

   ```bash
   python manage.py createsuperuser
   ```

6. **Iniciar o servidor local**

   ```bash
   python manage.py runserver
   ```

A API ficará disponível em `http://127.0.0.1:8000/api/` e o painel administrativo em `http://127.0.0.1:8000/admin/`.

## 🔐 Autenticação e permissões

A API usa a política **somente leitura para anônimos**:

| Operação | Quem pode |
|---|---|
| `GET` (consultar) | Qualquer pessoa, sem login |
| `POST`, `PUT`, `PATCH`, `DELETE` | Apenas usuários autenticados |

A autenticação é feita via **HTTP Basic Auth**, com o usuário criado no passo 5 da instalação. Sem login, uma tentativa de escrita retorna `401` ou `403`.

No **Postman** ou **Insomnia**, escolha a aba *Authorization* → *Basic Auth* e informe usuário e senha. No terminal (Linux, Mac ou Git Bash):

```bash
curl -u meu_usuario:minha_senha -X POST http://127.0.0.1:8000/api/lojas/ \
  -H "Content-Type: application/json" \
  -d '{"nome": "KaBuM!", "site": "https://www.kabum.com.br"}'
```

## 🔗 Endpoints

Base URL: `http://127.0.0.1:8000/api/`

Os três recursos (`lojas`, `componentes` e `precos`) oferecem o CRUD completo:

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/api/{recurso}/` | Lista os registros (paginada) |
| `POST` | `/api/{recurso}/` | Cria um registro 🔒 |
| `GET` | `/api/{recurso}/{id}/` | Detalha um registro |
| `PUT` / `PATCH` | `/api/{recurso}/{id}/` | Atualiza um registro (total / parcial) 🔒 |
| `DELETE` | `/api/{recurso}/{id}/` | Remove um registro 🔒 |

🔒 = exige autenticação.

### Paginação

As listagens retornam 20 itens por página, neste formato:

```json
{
  "count": 45,
  "next": "http://127.0.0.1:8000/api/precos/?page=2",
  "previous": null,
  "results": [ ... ]
}
```

Use `?page=2`, `?page=3` etc. para navegar.

### 🏪 Lojas — `/api/lojas/`

| Campo | Tipo | Obrigatório | Observação |
|---|---|---|---|
| `nome` | texto (até 100) | sim | |
| `site` | URL | não | |

**Exemplo de payload (`POST`):**

```json
{
  "nome": "KaBuM!",
  "site": "https://www.kabum.com.br"
}
```

### 💻 Componentes — `/api/componentes/`

| Campo | Tipo | Obrigatório | Observação |
|---|---|---|---|
| `nome` | texto (até 150) | sim | |
| `categoria` | texto (até 100) | sim | Ex.: "Placa de Vídeo", "Processador" |

**Exemplo de payload (`POST`):**

```json
{
  "nome": "Placa de Vídeo RX 6600",
  "categoria": "Placa de Vídeo"
}
```

### 📈 Histórico de preços — `/api/precos/`

Cada registro representa o preço de um componente em uma loja em determinada data.

| Campo | Tipo | Obrigatório | Observação |
|---|---|---|---|
| `componente` | ID | sim | ID de um componente existente |
| `loja` | ID | sim | ID de uma loja existente |
| `preco` | decimal (2 casas) | sim | Mínimo de `0.01` |
| `data_coleta` | data `AAAA-MM-DD` | não | Se omitida, usa a data de hoje |

**Exemplo de payload (`POST`):**

```json
{
  "componente": 1,
  "loja": 1,
  "preco": "1499.90",
  "data_coleta": "2026-10-05"
}
```

### 📊 Rotas customizadas (análises para decisão de compra)

#### Menor preço atual de uma peça

`GET /api/componentes/{id}/menor_preco/`

Considera o **preço mais recente de cada loja** e retorna o registro com o menor valor entre eles, ou seja, indica onde a peça está mais barata **hoje**. Preços antigos que já foram superados por registros mais novos da mesma loja são ignorados.

**Resposta (`200 OK`):**

```json
{
  "id": 7,
  "componente": 1,
  "loja": 2,
  "preco": "1199.90",
  "data_coleta": "2026-10-05"
}
```

**Resposta (`404 Not Found`)**, quando a peça ainda não tem preços cadastrados:

```json
{
  "mensagem": "Ainda não há preços registrados para esta peça."
}
```

#### Dados para gráfico de variação (últimos 6 meses)

`GET /api/componentes/{id}/grafico/`

Retorna a flutuação de preço da peça nos últimos 180 dias, ordenada por data e já formatada para alimentar um gráfico de linhas.

**Resposta (`200 OK`):**

```json
{
  "componente": "Placa de Vídeo RX 6600",
  "total_registros": 3,
  "historico": [
    { "data": "2026-08-10", "preco": 1599.9, "loja": "KaBuM!" },
    { "data": "2026-09-15", "preco": 1499.9, "loja": "KaBuM!" },
    { "data": "2026-10-05", "preco": 1199.9, "loja": "Pichau" }
  ]
}
```

## ✅ Regras de negócio e validações

- O **preço** deve ser maior ou igual a `0.01`. Valores zero ou negativos retornam `400 Bad Request`.
- Não é possível cadastrar **dois preços para o mesmo componente, na mesma loja, no mesmo dia**. A tentativa retorna `400 Bad Request`. Para corrigir um valor, use `PUT` ou `PATCH` no registro existente.
- Lojas e componentes que possuem histórico de preços **não podem ser apagados**, para não perder o histórico.
- Referências inexistentes (por exemplo, um `componente` com ID que não existe) retornam `400 Bad Request`.

## 🧪 Testes automatizados

O projeto possui testes de API cobrindo as rotas customizadas, as validações e as permissões. Para executá-los:

```bash
python manage.py test
```

Os testes usam um banco temporário e **não alteram** o `db.sqlite3`.

## 📁 Estrutura do projeto

```
api-hardware-backend/
├── hardware/                 # App principal
│   ├── migrations/           # Histórico de alterações do banco
│   ├── admin.py              # Configuração do painel /admin/
│   ├── models.py             # Loja, Componente e HistoricoPreco
│   ├── serializers.py        # Conversão dos models para JSON
│   ├── tests.py              # Testes automatizados
│   └── views.py              # ViewSets e rotas customizadas
├── projeto_hardware/         # Configurações do projeto
│   ├── settings.py
│   └── urls.py               # Registro das rotas da API
├── manage.py
├── requirements.txt
└── README.md
```

## 🔧 Variáveis de ambiente

Por padrão, o projeto roda com configurações de **desenvolvimento**. As variáveis abaixo são opcionais e permitem alterar esse comportamento:

| Variável | Padrão | Descrição |
|---|---|---|
| `SECRET_KEY` | chave de desenvolvimento | Chave secreta do Django. **Defina uma própria** se for publicar o projeto. |
| `DEBUG` | `True` | Use `False` em produção. |

> ⚠️ Este projeto é acadêmico. Para uso real em produção seria necessário, no mínimo, definir `SECRET_KEY` própria, usar `DEBUG=False`, configurar `ALLOWED_HOSTS` e trocar o SQLite por um banco como PostgreSQL.