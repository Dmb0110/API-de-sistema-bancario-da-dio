# 🐳 Docker - Guia Rápido de Referência

## Visão Geral da Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                        Host Machine                          │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                   Docker Network                      │   │
│  │          (banco_network - isolada)                   │   │
│  │                                                       │   │
│  │  ┌────────────────┐  ┌────────────────┐             │   │
│  │  │   FastAPI API  │  │  PostgreSQL    │             │   │
│  │  │                │  │                │             │   │
│  │  │ :8000          │  │ :5432          │             │   │
│  │  │ (asginc)       │  │ (database)     │             │   │
│  │  └────────────────┘  └────────────────┘             │   │
│  │                                                       │   │
│  │  ┌────────────────┐                                  │   │
│  │  │   pgAdmin      │                                  │   │
│  │  │                │                                  │   │
│  │  │ :5050          │                                  │   │
│  │  │ (web UI)       │                                  │   │
│  │  └────────────────┘                                  │   │
│  │                                                       │   │
│  │  Volumes Persistentes:                              │   │
│  │  └─ postgres_data (dados do banco)                  │   │
│  │                                                       │   │
│  └──────────────────────────────────────────────────────┘   │
│                          ▲                                    │
│                          │                                    │
│                    Portas Expostas                            │
│                          │                                    │
│  localhost:8000 ◄────────┤                                   │
│  localhost:5432 ◄────────┤                                   │
│  localhost:5050 ◄────────┘                                   │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## 📝 Checklist de Uso

### Primeira Vez

- [ ] Instale Docker Desktop
- [ ] Clone/acesse o projeto
- [ ] Copie `.env.example` para `.env`
- [ ] Execute `make setup` (ou script manual)
- [ ] Aguarde 30-60 segundos
- [ ] Acesse http://localhost:8000/docs
- [ ] Registre um usuário
- [ ] Faça login
- [ ] Crie um cliente

### Desenvolvimento Diário

- [ ] `make up` para iniciar
- [ ] Desenvolva normalmente (código recarrega automaticamente)
- [ ] `make test` para rodar testes
- [ ] `make logs` para ver o que está acontecendo
- [ ] `make down` para parar quando terminar

---

## 🔄 Fluxo Básico

### Inicializar

```bash
make setup
# ou
docker-compose up -d
```

### Desenvolver

```bash
# Edite seus arquivos .py
# O código recarrega automaticamente!

# Ver logs em tempo real
make logs
```

### Testar

```bash
# Rodar todos os testes
make test

# Rodar com verbosidade
make test-v

# Rodar teste específico
make test-specific
```

### Parar

```bash
make down
# Dados persistem! Próxima vez só precisa: make up
```

---

## 🔌 Conectando ao Banco

### Via psql (CLI)

```bash
make db-shell
# Dentro do psql:
\dt                        # Listar tabelas
SELECT * FROM users;       # Ver usuários
\d clientes                # Descrever tabela
\q                         # Sair
```

### Via pgAdmin (GUI)

```
1. Acesse http://localhost:5050
2. Email: admin@example.com
3. Senha: admin
4. Add Server (host: postgres, user: bancario)
```

### Via Python

```python
# Dentro do container
docker-compose exec api bash

# Python interativo
python
>>> import asyncio
>>> from sqlalchemy import select
>>> from app.models.models_cliente import Cliente
>>> # ... suas queries
```

---

## 🧠 Entender Logs

### Log Normal da API
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### Erro: Database Connection
```
asyncpg.exceptions.InvalidCatalogNameError: database "banco_bancario" does not exist
```
**Solução:** Aguarde PostgreSQL inicializar (30-60 segundos)

### Erro: Port em Uso
```
Address already in use
```
**Solução:** `docker-compose down` ou `make clean`

---

## 🚀 Comandos Mais Usados

### Gerenciar

| Comando | Resultado |
|---------|-----------|
| `make up` | Inicia |
| `make down` | Para |
| `make restart` | Reinicia |
| `make clean` | Limpa |
| `make ps` | Status |

### Monitorar

| Comando | Resultado |
|---------|-----------|
| `make logs` | Logs de tudo |
| `make logs-api` | Logs da API |
| `make logs-db` | Logs do banco |

### Acessar

| Comando | Resultado |
|---------|-----------|
| `make shell` | Terminal container |
| `make db-shell` | Terminal PostgreSQL |

### Testar

| Comando | Resultado |
|---------|-----------|
| `make test` | Rodar testes |
| `make test-v` | Testes verbose |

---

## 🔐 Configurações de Segurança

### Em Desenvolvimento
```env
SECRET_KEY=dev-secret (OK para dev)
DATABASE_PASSWORD=senha123 (OK para dev)
```

### Em Produção
```env
SECRET_KEY=gere_uma_chave_aleatoria_super_segura_aqui
DATABASE_PASSWORD=senha_muito_complexa_com_simbolos!@#
```

### Nunca Commite
- ✅ `.env` (git ignored)
- ❌ Senhas em código
- ❌ Keys de produção

---

## 📊 Monitoramento

### Recursos do Container

```bash
# Ver uso de CPU/Memória
docker stats
```

### Tamanho da Imagem

```bash
# Ver tamanho
docker images banco_api

# Reduzir:
docker system prune -a
```

### Limpeza

```bash
# Remove volumes (⚠️ deleta dados)
docker-compose down -v

# Remove imagens não usadas
docker image prune
```

---

## 🐛 Troubleshooting Rápido

| Problema | Solução |
|----------|---------|
| Porta em uso | `docker-compose down` |
| Container não inicia | `make logs` |
| Banco não conecta | Aguarde 30-60s |
| Dados desapareceram | Não execute `down -v` |
| Quer limpar tudo | `make reset` |
| Quer ver dados | pgAdmin em :5050 |

---

## 📈 Próximos Passos Avançados

1. **Adicionar Cache Redis**
   - Docker image: redis:alpine
   - Usar como cache de sessions

2. **Adicionar Celery (Async Tasks)**
   - Para enviar emails
   - Para gerar relatórios

3. **Setup CI/CD (GitHub Actions)**
   - Build automático
   - Testes automáticos
   - Deploy automático

4. **Monitoramento (Prometheus + Grafana)**
   - Métricas da API
   - Métricas do banco
   - Dashboards

---

## 🎓 Leitura Recomendada

- [QUICK_START.md](QUICK_START.md) - Comece aqui
- [DOCKER.md](DOCKER.md) - Detalhes completos
- [README.md](README.md) - Documentação API
- Docker docs: https://docs.docker.com/
- FastAPI docs: https://fastapi.tiangolo.com/

---

**Happy coding! 🎉**
