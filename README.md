# 🏦 API de Sistema Bancário - Documentação Completa

## 📋 Sumário

- [Visão Geral](#visão-geral)
- [Tecnologias](#tecnologias)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Docker (Recomendado)](#-docker-recomendado)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Modelos de Dados](#modelos-de-dados)
- [Rotas da API](#rotas-da-api)
- [Funções de Serviço](#funções-de-serviço)
- [Autenticação](#autenticação)
- [Exemplos de Uso](#exemplos-de-uso)
- [Testes](#testes)

---

## 🎯 Visão Geral

Esta é uma API RESTful completa de um sistema bancário desenvolvida com **FastAPI** e **SQLAlchemy**. O projeto oferece funcionalidades para:

- ✅ Gerenciamento de usuários (registro e login com JWT)
- ✅ Cadastro e consulta de clientes
- ✅ Criação e gerenciamento de contas bancárias
- ✅ Realização de transações (depósitos e saques)
- ✅ Listagem de clientes e contas
- ✅ Consulta de histórico de transações

---

## 🛠️ Tecnologias

- **FastAPI** - Framework web assíncrono
- **SQLAlchemy** - ORM para banco de dados
- **PostgreSQL/SQLite** - Banco de dados
- **Pydantic** - Validação de dados
- **JWT (Python-Jose)** - Autenticação por tokens
- **Passlib + Bcrypt** - Hash seguro de senhas
- **Alembic** - Migrations do banco de dados
- **pytest** - Framework de testes
- **httpx** - Cliente HTTP assíncrono para testes

---

## 📦 Instalação

### Pré-requisitos
- Python 3.8+
- pip ou conda
- PostgreSQL (ou SQLite para desenvolvimento)

### Passos de Instalação

1. **Clone o repositório**
```bash
cd "api de sistema bancario da dio"
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure o arquivo .env** (veja seção de configuração)

5. **Execute as migrations**
```bash
alembic upgrade head
```

6. **Inicie o servidor**
```bash
uvicorn app.main:app --reload
```

A API estará disponível em: `http://localhost:8000`

---

## ⚙️ Configuração

### Arquivo .env

Crie um arquivo `.env` na raiz do projeto:

```env
# Banco de Dados
DATABASE_URL=postgresql+asyncpg://usuario:senha@localhost/banco_bancario

# Para desenvolvimento com SQLite:
# DATABASE_URL=sqlite+aiosqlite:///./database.db

# Autenticação
SECRET_KEY=sua-chave-secreta-super-segura-aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Variáveis de Ambiente Importantes

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `DATABASE_URL` | String de conexão do BD | Obrigatório |
| `SECRET_KEY` | Chave para assinar JWT | `dev-secret` |
| `ALGORITHM` | Algoritmo de codificação JWT | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Minutos até token expirar | `30` |

---

g## � Docker (Recomendado)

A forma mais fácil de rodar a aplicação é usando **Docker** e **Docker Compose**.

### Quick Start com Docker

```bash
# 1. Clonar/acessar projeto
cd "api de sistema bancario da dio"

# 2. Copiar arquivo de exemplo
cp .env.example .env

# 3. Iniciar com Docker
docker-compose up -d

# 4. Verificar status
docker-compose ps
```

### Acessar Serviços

- **API (Swagger):** http://localhost:8000/docs
- **API (ReDoc):** http://localhost:8000/redoc
- **pgAdmin:** http://localhost:5050 (admin@example.com / admin)

### Comandos Docker Úteis

```bash
# Ver logs
docker-compose logs -f api

# Executar testes
docker-compose exec api pytest -v

# Acessar shell do container
docker-compose exec api bash

# Acessar PostgreSQL
docker-compose exec postgres psql -U bancario -d banco_bancario

# Parar serviços
docker-compose down
```

### Usar Makefile (mais fácil)

```bash
make help        # Ver todos os comandos
make setup       # Setup inicial
make up          # Iniciar serviços
make down        # Parar serviços
make logs        # Ver logs
make test        # Rodar testes
make restart     # Reiniciar
make clean       # Limpar tudo
```

Para detalhes completos, consulte [DOCKER.md](DOCKER.md)

---

```
app/
├── __init__.py
├── main.py                          # Aplicação principal FastAPI
├── rotas_principais.py              # Agregador de rotas
│
├── autenticacao_bancaria/
│   ├── __init__.py
│   └── auth.py                      # Funções de autenticação JWT
│
├── core/
│   ├── __init__.py
│   └── config.py                    # Configurações da aplicação
│
├── database/
│   ├── __init__.py
│   └── session.py                   # Configuração da sessão do BD
│
├── models/
│   ├── __init__.py
│   ├── models_auth.py              # Modelo User
│   ├── models_cliente.py           # Modelo Cliente
│   ├── models_conta.py             # Modelo Conta
│   └── models_transacao.py         # Modelo Transacao
│
├── routers/
│   ├── __init__.py
│   ├── routers_registro_login.py   # Rotas de autenticação
│   ├── routers_banco.py            # Rotas principais de banco
│   └── routers_get.py              # Rotas de listagem/consulta
│
├── schemas/
│   ├── __init__.py
│   ├── schemas_auth.py             # Schemas de autenticação
│   ├── schemas_do_cliente.py       # Schemas de cliente
│   ├── schemas_da_conta.py         # Schemas de conta
│   └── schemas_da_transacao.py     # Schemas de transação
│
└── service/
    ├── __init__.py
    ├── service_registro_login.py   # Lógica de autenticação
    ├── service_bancario.py         # Lógica de operações bancárias
    └── service_get.py              # Lógica de listagem

tests2/                             # Testes simples (1 por rota)
test_main.py                        # Suite completa de testes
conftest.py                         # Configuração de testes
pytest.ini                          # Configuração do pytest
```

---

## 🗄️ Modelos de Dados

### 1. User (Autenticação)

```python
class User(Base):
    __tablename__ = "users"
    
    id: int                          # ID único
    username: str (único)            # Nome de usuário
    hashed_password: str             # Senha com hash bcrypt
```

**Relacionamentos:** Nenhum (tabela simples de usuários)

---

### 2. Cliente

```python
class Cliente(Base):
    __tablename__ = "clientes"
    
    id: int                          # ID único
    nome: str                        # Nome completo
    cpf: str (único)                # CPF (identificador único)
    endereco: str                   # Endereço residencial
    data_nascimento: str            # Data de nascimento (YYYY-MM-DD)
    
    # Relacionamentos
    contas: List[Conta]            # Contas relacionadas ao cliente
```

**Validações:**
- CPF deve ser único no banco
- Todos os campos são obrigatórios

---

### 3. Conta

```python
class Conta(Base):
    __tablename__ = "contas"
    
    id: int                         # ID único
    numero: int (único)             # Número da conta
    saldo: float                    # Saldo atual (padrão: 0.0)
    agencia: str                    # Agência (padrão: "0001")
    cliente_id: int (FK)            # ID do cliente proprietário
    
    # Relacionamentos
    cliente: Cliente                # Cliente proprietário
    transacoes: List[Transacao]    # Histórico de transações
    
    # Propriedades
    @property titular: str          # Nome do cliente (proprietário)
    @property historico: List       # Lista de transações
```

**Validações:**
- Número da conta deve ser único
- Deve estar relacionada a um cliente existente

---

### 4. Transacao

```python
class Transacao(Base):
    __tablename__ = "transacoes"
    
    id: int                         # ID único
    tipo_de_transacao: str          # "deposito" ou "saque"
    valor: float                    # Valor da transação
    data: datetime                  # Data/hora da transação
    conta_id: int (FK)              # ID da conta
    
    # Relacionamentos
    conta: Conta                    # Conta envolvida na transação
```

**Validações:**
- Tipo deve ser "deposito" ou "saque"
- Valor deve ser positivo

---

## 🚀 Rotas da API

### 📍 Prefixo Base
- URL Base: `http://localhost:8000`
- Documentação: `http://localhost:8000/docs`

---

### 🔐 AUTENTICAÇÃO (/auth)

#### 1. **Registrar Novo Usuário**
```http
POST /auth/register
```

**Descrição:** Cria uma nova conta de usuário

**Request Body:**
```json
{
  "username": "joao_silva",
  "password": "senha123"
}
```

**Response (201 - OK):**
```json
{
  "id": 1,
  "username": "joao_silva"
}
```

**Possíveis Erros:**
- `400` - Usuário já existe
- `422` - Dados inválidos

**Função Responsável:** `ServiceAuth.registrar_usuario()`

---

#### 2. **Login do Usuário**
```http
POST /auth/login
```

**Descrição:** Autentica o usuário e retorna um JWT token

**Request Body:**
```json
{
  "username": "joao_silva",
  "password": "senha123"
}
```

**Response (200 - OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Possíveis Erros:**
- `400` - Credenciais inválidas
- `422` - Dados inválidos

**Função Responsável:** `ServiceAuth.logar_usuario()`

---

### 🏦 OPERAÇÕES BANCÁRIAS (/banco)

#### 1. **Criar Cliente**
```http
POST /banco/clientes/
```

**Descrição:** Registra um novo cliente no sistema bancário

**Request Body:**
```json
{
  "nome": "João da Silva Santos",
  "cpf": "12345678901",
  "endereco": "Rua das Flores, 123, Apt 456",
  "data_nascimento": "1990-05-15"
}
```

**Response (201 - CREATED):**
```json
{
  "id": 1,
  "nome": "João da Silva Santos",
  "cpf": "12345678901",
  "endereco": "Rua das Flores, 123, Apt 456",
  "data_nascimento": "1990-05-15",
  "contas": []
}
```

**Possíveis Erros:**
- `400` - CPF já existe no sistema
- `422` - Dados inválidos

**Função Responsável:** `ServiceBancario.criar_cliente()`

---

#### 2. **Criar Conta Bancária**
```http
POST /banco/contas/
```

**Descrição:** Cria uma nova conta bancária para um cliente existente

**Request Body:**
```json
{
  "numero": 123456,
  "cpf": "12345678901"
}
```

**Response (201 - CREATED):**
```json
{
  "numero": 123456,
  "agencia": "0001",
  "saldo": 0.0,
  "titular": "João da Silva Santos",
  "historico": []
}
```

**Possíveis Erros:**
- `404` - Cliente não encontrado
- `400` - Número de conta já existe
- `422` - Dados inválidos

**Função Responsável:** `ServiceBancario.criar_conta()`

---

#### 3. **Consultar Conta**
```http
GET /banco/contas/{numero}
```

**Parâmetros:**
- `numero` (path) - Número da conta

**Response (200 - OK):**
```json
{
  "numero": 123456,
  "agencia": "0001",
  "saldo": 5000.00,
  "titular": "João da Silva Santos",
  "historico": [
    {
      "tipo_de_transacao": "deposito",
      "valor": 5000.00,
      "data": "12-01-2026 10:30:45"
    }
  ]
}
```

**Possíveis Erros:**
- `404` - Conta não encontrada

**Função Responsável:** `ServiceBancario.consultar_conta()`

---

#### 4. **Realizar Transação (Depósito/Saque)**
```http
POST /banco/transacoes/
```

**Requer Autenticação:** ✅ Sim (JWT Token)

**Headers Obrigatórios:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "numero_conta": 123456,
  "tipo_de_transacao": "deposito",
  "valor": 1000.00
}
```

**Tipos de Transação:**
- `"deposito"` - Adiciona saldo à conta
- `"saque"` - Remove saldo da conta

**Response (200 - OK):**
```json
{
  "mensagem": "Depósito realizado com sucesso"
}
```

**Possíveis Erros:**
- `403` - Não autenticado
- `404` - Conta não encontrada
- `400` - Saldo insuficiente (para saques) ou tipo inválido
- `422` - Dados inválidos

**Função Responsável:** `ServiceBancario.criar_transacao()`

---

#### 5. **Rota Protegida (Teste de Autenticação)**
```http
GET /banco/protected
```

**Requer Autenticação:** ✅ Sim (JWT Token)

**Headers Obrigatórios:**
```
Authorization: Bearer {access_token}
```

**Response (200 - OK):**
```json
{
  "msg": "Bem-vindo joao_silva, você acessou uma rota protegida!"
}
```

**Possíveis Erros:**
- `403` - Não autenticado ou token inválido/expirado

---

### 📊 LISTAGEM E CONSULTA (/get)

#### 1. **Listar Todos os Clientes**
```http
GET /get/clientes
```

**Response (200 - OK):**
```json
[
  {
    "id": 1,
    "nome": "João da Silva Santos",
    "cpf": "12345678901",
    "endereco": "Rua das Flores, 123",
    "data_nascimento": "1990-05-15",
    "contas": [
      {
        "numero": 123456,
        "agencia": "0001",
        "saldo": 5000.00,
        "titular": "João da Silva Santos",
        "historico": []
      }
    ]
  }
]
```

**Possíveis Erros:**
- `404` - Nenhum cliente encontrado

**Função Responsável:** `ServiceGet.listar_clientes()`

---

#### 2. **Listar Todas as Contas**
```http
GET /get/contas
```

**Response (200 - OK):**
```json
[
  {
    "numero": 123456,
    "agencia": "0001",
    "saldo": 5000.00,
    "titular": "João da Silva Santos",
    "historico": []
  }
]
```

**Possíveis Erros:**
- `404` - Nenhuma conta encontrada

**Função Responsável:** `ServiceGet.listar_contas()`

---

#### 3. **Consultar Cliente Específico com Contas**
```http
GET /get/cliente/{cliente_id}
```

**Parâmetros:**
- `cliente_id` (path) - ID do cliente

**Response (200 - OK):**
```json
{
  "id": 1,
  "nome": "João da Silva Santos",
  "cpf": "12345678901",
  "endereco": "Rua das Flores, 123",
  "data_nascimento": "1990-05-15",
  "contas": [
    {
      "numero": 123456,
      "agencia": "0001",
      "saldo": 5000.00,
      "titular": "João da Silva Santos",
      "historico": []
    }
  ]
}
```

**Possíveis Erros:**
- `404` - Cliente não encontrado

**Função Responsável:** `ServiceGet.lista_cliente_contas()`

---

## 🔧 Funções de Serviço

### ServiceAuth (service_registro_login.py)

#### 1. `registrar_usuario(data: RegisterUsuario, session: AsyncSession)`
- **Parâmetros:** 
  - `data` - Objeto com username e password
  - `session` - Sessão do banco de dados
- **Retorna:** `UsuarioOut | str`
- **Lógica:**
  - Verifica se username já existe
  - Se existe: retorna `'usuario_ja_existe'`
  - Se não existe: cria novo usuário com senha com hash
  - Retorna dados do novo usuário

#### 2. `logar_usuario(data: LoginUsuario, session: AsyncSession)`
- **Parâmetros:**
  - `data` - Objeto com username e password
  - `session` - Sessão do banco de dados
- **Retorna:** `TokenOut | str`
- **Lógica:**
  - Procura usuário no banco
  - Verifica se senha está correta
  - Se inválido: lança HTTPException (401)
  - Se válido: gera JWT token
  - Retorna token de acesso

---

### ServiceBancario (service_bancario.py)

#### 1. `criar_cliente(criar: ClienteIn, session: AsyncSession)`
- **Parâmetros:**
  - `criar` - Objeto com dados do cliente
  - `session` - Sessão do banco de dados
- **Retorna:** `Cliente | str`
- **Lógica:**
  - Verifica se CPF já existe
  - Se existe: retorna `'cliente_com_esse_cpf_ja_existe'`
  - Se não: cria novo cliente
  - Commit no banco
  - Retorna cliente criado

#### 2. `criar_conta(criar: ContaIn, session: AsyncSession)`
- **Parâmetros:**
  - `criar` - Objeto com número e CPF do cliente
  - `session` - Sessão do banco de dados
- **Retorna:** `Conta | str`
- **Lógica:**
  - Procura cliente pelo CPF
  - Se não encontrado: retorna `'cliente_nao_encontrado'`
  - Verifica se número da conta já existe
  - Se existe: retorna `'conta_ja_existe'`
  - Se não: cria nova conta com saldo 0.0 e agência "0001"
  - Commit no banco
  - Retorna conta criada

#### 3. `consultar_conta(numero: int, session: AsyncSession)`
- **Parâmetros:**
  - `numero` - Número da conta
  - `session` - Sessão do banco de dados
- **Retorna:** `ContaOut | str`
- **Lógica:**
  - Procura conta pelo número
  - Se não encontrada: retorna `'conta_nao_encontrada'`
  - Se encontrada: formata resposta com:
    - Número, agência, saldo
    - Nome do titular
    - Histórico de transações formatado
  - Retorna ContaOut

#### 4. `criar_transacao(transacao: TransacaoIn, session: AsyncSession)`
- **Parâmetros:**
  - `transacao` - Objeto com número da conta, tipo e valor
  - `session` - Sessão do banco de dados
- **Retorna:** `MensagemOut`
- **Lógica:**
  - Procura conta
  - Se não encontrada: retorna mensagem de erro
  - **Se tipo = "deposito":** adiciona valor ao saldo
  - **Se tipo = "saque":**
    - Verifica se saldo é suficiente
    - Se insuficiente: retorna mensagem de erro
    - Se suficiente: subtrai valor do saldo
  - Se tipo inválido: retorna mensagem de erro
  - Cria registro de transação
  - Commit no banco
  - Retorna mensagem de sucesso

---

### ServiceGet (service_get.py)

#### 1. `listar_clientes(session: AsyncSession)`
- **Parâmetros:**
  - `session` - Sessão do banco de dados
- **Retorna:** `List[Cliente] | str`
- **Lógica:**
  - Executa query para buscar todos os clientes
  - Se vazio: retorna `'clientes_nao_encontrados'`
  - Caso contrário: retorna lista de clientes

#### 2. `listar_contas(session: AsyncSession)`
- **Parâmetros:**
  - `session` - Sessão do banco de dados
- **Retorna:** `List[Conta] | str`
- **Lógica:**
  - Executa query para buscar todas as contas
  - Se vazio: retorna `'contas_nao_encontradas'`
  - Caso contrário: retorna lista de contas

#### 3. `lista_cliente_contas(cliente_id: int, session: AsyncSession)`
- **Parâmetros:**
  - `cliente_id` - ID do cliente
  - `session` - Sessão do banco de dados
- **Retorna:** `Cliente | str`
- **Lógica:**
  - Busca cliente pelo ID
  - Carrega relacionamento de contas (eager loading)
  - Se não encontrado: retorna `'cliente_nao_encontrado'`
  - Caso contrário: retorna cliente com suas contas

---

## 🔐 Autenticação

### Fluxo de Autenticação

```
1. Usuário faz POST em /auth/register
   ↓
2. Senha é feita hash com bcrypt
   ↓
3. Novo User é criado no banco
   ↓
4. Usuário faz POST em /auth/login
   ↓
5. Credenciais são verificadas
   ↓
6. JWT token é gerado e retornado
   ↓
7. Token é usado em Authorization header das requisições
```

### Funções de Autenticação (auth.py)

#### `hash_password(password: str) -> str`
- Converte senha em texto puro para hash bcrypt
- Usada no registro de usuários

#### `verify_password(plain: str, hashed: str) -> bool`
- Compara senha em texto puro com hash armazenado
- Retorna True/False

#### `create_token(sub: str) -> str`
- Gera JWT token com username como subject
- Token expira em 30 minutos (configurável)
- Codificado com SECRET_KEY

#### `verificar_token(credentials: HTTPAuthorizationCredentials) -> str`
- Valida token JWT
- Extrai username do payload
- Retorna username se válido
- Lança HTTPException (401) se inválido/expirado

### Usando Authorization Header

```bash
curl -X GET http://localhost:8000/banco/protected \
  -H "Authorization: Bearer seu_token_aqui"
```

---

## 📝 Exemplos de Uso

### Exemplo Completo: Fluxo Bancário

#### 1. Registrar Usuário
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "joao_silva",
    "password": "senha123"
  }'
```

#### 2. Fazer Login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "joao_silva",
    "password": "senha123"
  }'

# Response:
# {
#   "access_token": "eyJhbGci...",
#   "token_type": "bearer"
# }

TOKEN="eyJhbGci..."
```

#### 3. Criar Cliente
```bash
curl -X POST http://localhost:8000/banco/clientes/ \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João da Silva",
    "cpf": "12345678901",
    "endereco": "Rua das Flores, 123",
    "data_nascimento": "1990-05-15"
  }'
```

#### 4. Criar Conta
```bash
curl -X POST http://localhost:8000/banco/contas/ \
  -H "Content-Type: application/json" \
  -d '{
    "numero": 123456,
    "cpf": "12345678901"
  }'
```

#### 5. Fazer Depósito
```bash
curl -X POST http://localhost:8000/banco/transacoes/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "numero_conta": 123456,
    "tipo_de_transacao": "deposito",
    "valor": 5000.00
  }'
```

#### 6. Fazer Saque
```bash
curl -X POST http://localhost:8000/banco/transacoes/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "numero_conta": 123456,
    "tipo_de_transacao": "saque",
    "valor": 1000.00
  }'
```

#### 7. Consultar Conta
```bash
curl -X GET http://localhost:8000/banco/contas/123456
```

#### 8. Listar Clientes
```bash
curl -X GET http://localhost:8000/get/clientes
```

---

## 🧪 Testes

### Rodando os Testes

```bash
# Executar todos os testes
pytest

# Com verbosidade
pytest -v

# Apenas testes da pasta tests2
pytest tests2/ -v

# Teste específico
pytest tests2/test_auth_register.py -v

# Com cobertura
pytest --cov=app --cov-report=html
```

### Estrutura de Testes

**test_main.py** - Suite completa com 41 testes
- Testes de autenticação
- Testes de clientes
- Testes de contas
- Testes de transações
- Testes de rotas protegidas
- Testes de fluxo completo
- Testes de validações

**tests2/** - Um teste simples por rota
- test_auth_register.py
- test_auth_login.py
- test_banco_criar_cliente.py
- test_banco_criar_conta.py
- test_banco_consultar_conta.py
- test_banco_transacao.py
- test_banco_protected.py
- test_get_listar_clientes.py
- test_get_listar_contas.py
- test_get_consultar_cliente.py

### Banco de Testes

Os testes usam **SQLite em memória** para:
- Isolamento entre testes
- Rapidez de execução
- Sem necessidade de BD externo

---

## 📊 Diagramas

### Fluxo de Dados - Criação de Conta

```
POST /banco/contas/
    ↓
Router: criar2()
    ↓
ServiceBancario.criar_conta()
    ├─ Busca Cliente por CPF
    │  └─ Se não existir: erro 404
    ├─ Verifica se Conta já existe
    │  └─ Se existir: erro 400
    └─ Cria nova Conta
       ├─ numero: informado
       ├─ cliente_id: do cliente encontrado
       ├─ saldo: 0.0
       └─ agencia: "0001"
    ↓
Persiste no BD
    ↓
Response: ContaOut (201 Created)
```

### Fluxo de Dados - Transação

```
POST /banco/transacoes/
    ↓
Router: criar3() [requer JWT]
    ↓
ServiceBancario.criar_transacao()
    ├─ Busca Conta por número
    │  └─ Se não existir: erro 404
    ├─ Verifica tipo_de_transacao
    │  ├─ "deposito": saldo += valor
    │  ├─ "saque": 
    │  │  ├─ Se saldo < valor: erro 400
    │  │  └─ Se saldo >= valor: saldo -= valor
    │  └─ outro: erro 400
    └─ Cria novo registro Transacao
       ├─ tipo_de_transacao
       ├─ valor
       ├─ data: datetime.now()
       └─ conta_id
    ↓
Persiste Transacao e Conta (com novo saldo)
    ↓
Response: MensagemOut (200 OK)
```

---

## 🐛 Códigos de Erro Comuns

| Código | Descrição | Causa |
|--------|-----------|-------|
| 200 | OK | Requisição bem-sucedida |
| 201 | Created | Recurso criado com sucesso |
| 400 | Bad Request | CPF duplicado, saldo insuficiente, tipo inválido |
| 401 | Unauthorized | Credenciais inválidas, token expirado |
| 403 | Forbidden | Sem autenticação (token não fornecido) |
| 404 | Not Found | Cliente, conta ou usuário não encontrado |
| 422 | Unprocessable Entity | Dados inválidos no request body |
| 500 | Internal Server Error | Erro no servidor |

---

## 📚 Dependências Principais

```
fastapi              # Framework web
uvicorn[standard]    # Servidor ASGI
sqlalchemy           # ORM
asyncpg              # Driver PostgreSQL assíncrono
python-dotenv        # Variáveis de ambiente
python-jose          # JWT
passlib[bcrypt]      # Hash de senhas
bcrypt               # Usado pelo passlib
alembic              # Migrations
pytest               # Testes
pytest-asyncio       # Testes assíncronos
httpx                # Cliente HTTP para testes
aiosqlite            # SQLite assíncrono para testes
```

---

## 🚀 Próximas Melhorias Sugeridas

- [ ] Adicionar operação de transferência entre contas
- [ ] Implementar filtros de data no histórico de transações
- [ ] Adicionar upload de documentos de cliente
- [ ] Implementar limites de transação
- [ ] Adicionar logs de segurança
- [ ] Implementar rate limiting
- [ ] Adicionar email de confirmação
- [ ] Implementar dashboard de análises
- [ ] Adicionar relatórios em PDF
- [ ] Implementar autenticação com 2FA

---

## 📞 Suporte

Para dúvidas ou issues, consulte:
- Documentação interativa: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- Código das rotas: pasta `app/routers/`
- Código dos serviços: pasta `app/service/`

---

## 📄 Licença

Este projeto é um exercício educacional da DIO (Digital Innovation One).

---

**Última atualização:** 12 de Janeiro de 2026
