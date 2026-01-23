# 🐳 Guia Docker - API de Sistema Bancário

## 📋 Visão Geral

Este guia explica como usar Docker e Docker Compose para executar a API de Sistema Bancário em containers, com PostgreSQL e pgAdmin inclusos.

## 🛠️ Pré-requisitos

- **Docker** 20.10+
- **Docker Compose** 1.29+

### Instalação do Docker

#### Windows/Mac
1. Baixe o [Docker Desktop](https://www.docker.com/products/docker-desktop)
2. Instale seguindo as instruções do instalador
3. Verifique a instalação:
```bash
docker --version
docker-compose --version
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install docker.io docker-compose

# Adicionar seu usuário ao grupo docker (sem sudo)
sudo usermod -aG docker $USER
```

---

## 🚀 Iniciando a Aplicação

### 1. Clone/Configure o Projeto

```bash
cd "api de sistema bancario da dio"
```

### 2. Crie o arquivo .env

Copie o arquivo `.env.example` para `.env` e configure conforme necessário:

```bash
cp .env.example .env
```

Valores padrão já estão configurados. Para produção, altere:
- `POSTGRES_PASSWORD` - Senha do banco
- `SECRET_KEY` - Chave de segurança JWT

### 3. Inicie os Containers

```bash
# Inicia todos os serviços em background
docker-compose up -d

# Ou com logs em tempo real
docker-compose up
```

**Primeira execução:** Pode levar alguns minutos para baixar as imagens.

### 4. Verifique o Status

```bash
# Ver status dos containers
docker-compose ps

# Ver logs da API
docker-compose logs api

# Ver logs do PostgreSQL
docker-compose logs postgres
```

### 5. Acesse a Aplicação

- **API (Swagger):** http://localhost:8000/docs
- **API (ReDoc):** http://localhost:8000/redoc
- **pgAdmin:** http://localhost:5050

---

## 📊 Serviços Disponíveis

### PostgreSQL
- **Host:** postgres (dentro do Docker) / localhost (do host)
- **Porta:** 5432
- **Usuário:** bancario
- **Senha:** senha123
- **Database:** banco_bancario

### FastAPI
- **Host:** localhost
- **Porta:** 8000
- **URL:** http://localhost:8000

### pgAdmin (Gerenciador PostgreSQL)
- **URL:** http://localhost:5050
- **Email:** admin@example.com
- **Senha:** admin

---

## 🔧 Comandos Úteis

### Gerenciar Containers

```bash
# Iniciar serviços
docker-compose up -d

# Parar serviços
docker-compose down

# Parar e remover volumes (limpa dados)
docker-compose down -v

# Reiniciar um serviço
docker-compose restart api

# Ver status
docker-compose ps
```

### Logs

```bash
# Ver logs de todos os serviços
docker-compose logs -f

# Ver logs de um serviço específico
docker-compose logs -f api
docker-compose logs -f postgres

# Ver últimas 100 linhas
docker-compose logs --tail=100 api
```

### Executar Comandos no Container

```bash
# Acessar shell da API
docker-compose exec api bash

# Executar comando Python na API
docker-compose exec api python -c "print('Hello')"

# Acessar PostgreSQL via CLI
docker-compose exec postgres psql -U bancario -d banco_bancario
```

### Banco de Dados

```bash
# Acessar psql no postgres
docker-compose exec postgres psql -U bancario -d banco_bancario

# Dentro do psql:
# \dt                    - Lista tabelas
# \d clientes            - Descreve tabela
# SELECT * FROM users;   - Query básica
# \q                     - Sair
```

---

## 🧪 Executar Testes

### No Container

```bash
# Executar todos os testes
docker-compose exec api pytest

# Com verbosidade
docker-compose exec api pytest -v

# Apenas testes da pasta tests2
docker-compose exec api pytest tests2/ -v

# Com cobertura
docker-compose exec api pytest --cov=app --cov-report=html
```

### Localmente

```bash
# Se preferir rodar sem Docker
python -m pytest -v
```

---

## 📁 Estrutura de Arquivos Docker

```
projeto/
├── Dockerfile              # Definição da imagem FastAPI
├── docker-compose.yml      # Orquestração dos serviços
├── .dockerignore           # Arquivos ignorados no build
├── .env.example            # Exemplo de configurações
└── .env                    # Configurações (git ignored)
```

---

## 🔐 Segurança em Produção

### Dockerfile Multi-Stage

O Dockerfile usa multi-stage build para:
- Reduzir tamanho da imagem final
- Remover ferramentas de desenvolvimento
- Melhorar segurança

### docker-compose.yml Produção

Para produção, crie um arquivo separado `docker-compose.prod.yml`:

```bash
# Usar em produção
docker-compose -f docker-compose.prod.yml up -d
```

### Alterações Recomendadas

1. **Variáveis de Ambiente:**
```bash
# Nunca commitar .env com valores reais
SECRET_KEY=gere-uma-chave-aleatoria-muito-longa-e-complexa
POSTGRES_PASSWORD=senha-muito-segura-aqui
```

2. **Remover Comando --reload:**
```yaml
command: uvicorn app.main:app --host 0.0.0.0 --port 8000
# Sem --reload em produção
```

3. **Limitar Recursos:**
```yaml
deploy:
  resources:
    limits:
      cpus: '1'
      memory: 512M
    reservations:
      cpus: '0.5'
      memory: 256M
```

4. **CORS em Produção:**
```python
# Em app/main.py
allow_origins=["https://seu-dominio.com"]  # Especificar domínios
```

---

## 🐛 Troubleshooting

### Erro: "Cannot connect to Docker daemon"

```bash
# Windows/Mac: Inicie o Docker Desktop
# Linux: Inicie o serviço
sudo systemctl start docker
```

### Erro: "Port 5432 already in use"

```bash
# Mudar porta no .env
POSTGRES_PORT=5433

# Ou parar container conflitante
docker stop <container_id>
```

### Erro: "Database connection refused"

```bash
# Verificar health do postgres
docker-compose ps

# Logs do postgres
docker-compose logs postgres

# Aguardar inicialização
docker-compose down -v
docker-compose up -d
sleep 10  # Aguardar 10 segundos
```

### Erro: "Module not found"

```bash
# Reconstruir imagem
docker-compose build --no-cache

# Reiniciar
docker-compose up -d
```

### Ver Dados Persistentes

```bash
# Listar volumes
docker volume ls

# Remover volume específico
docker volume rm banco_postgres_data
```

---

## 📊 Monitorando Containers

### Recursos em Tempo Real

```bash
# Dashboard do Docker
docker stats

# Inspecionar container
docker inspect <container_id>

# Ver histórico de eventos
docker events
```

### Verificar Conectividade

```bash
# Testar conexão API
curl http://localhost:8000/docs

# Testar conexão PostgreSQL
docker-compose exec api psql -h postgres -U bancario -d banco_bancario -c "SELECT 1;"
```

---

## 🔄 Atualizando a Aplicação

```bash
# Parar e remover containers antigos
docker-compose down

# Construir nova imagem
docker-compose build

# Iniciar com nova imagem
docker-compose up -d
```

---

## 🗄️ Usando pgAdmin para Gerenciar Banco

1. **Acesse pgAdmin:**
   - URL: http://localhost:5050
   - Email: admin@example.com
   - Senha: admin

2. **Adicione Servidor PostgreSQL:**
   - Clique em "Add New Server"
   - **Host:** postgres
   - **Usuário:** bancario
   - **Senha:** senha123
   - **Database:** banco_bancario

3. **Explore Tabelas:**
   - Veja estrutura de tabelas
   - Execute queries
   - Gerencie dados

---

## 📈 Performance

### Otimizações Implementadas

- ✅ Cache de dependências (pip)
- ✅ Multi-stage build (reduz imagem)
- ✅ Health checks (auto-recovery)
- ✅ Usuário não-root (segurança)
- ✅ Volume persistente para banco
- ✅ Network isolada (banco_network)

### Tamanho da Imagem

```bash
# Ver tamanho da imagem
docker images banco_api

# Típico: ~500-600 MB (com Python 3.11)
```

---

## 🚀 Deploy

### Opções de Deploy

#### Heroku
```bash
heroku create seu-app-bancario
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main
```

#### AWS (ECS/Fargate)
```bash
# Push para ECR
aws ecr get-login-password | docker login --username AWS --password-stdin <account>.dkr.ecr.<region>.amazonaws.com
docker tag banco_api:latest <account>.dkr.ecr.<region>.amazonaws.com/banco_api:latest
docker push <account>.dkr.ecr.<region>.amazonaws.com/banco_api:latest
```

#### DigitalOcean/VPS
```bash
# SSH no servidor
ssh user@seu-vps.com

# Clone repo
git clone <seu-repo>
cd projeto

# Inicie
docker-compose -f docker-compose.prod.yml up -d
```

---

## 📚 Recursos Adicionais

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Guide](https://docs.docker.com/compose/)
- [PostgreSQL Docker Image](https://hub.docker.com/_/postgres)
- [FastAPI with Docker](https://fastapi.tiangolo.com/deployment/docker/)

---

## ✅ Checklist de Setup

- [ ] Docker e Docker Compose instalados
- [ ] Arquivo `.env` criado
- [ ] `docker-compose up -d` executado
- [ ] Verificou `docker-compose ps`
- [ ] Acessou http://localhost:8000/docs
- [ ] Testou criar cliente via API
- [ ] Acessou pgAdmin em http://localhost:5050
- [ ] Rodou testes com `docker-compose exec api pytest`

---

**Última atualização:** 12 de Janeiro de 2026
