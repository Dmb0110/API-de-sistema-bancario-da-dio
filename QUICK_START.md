# ⚡ Quick Start - API Sistema Bancário

## 🚀 Inicie em 2 minutos!

### Com Docker (Recomendado ✅)

#### Windows (PowerShell)
```powershell
# 1. Clone/acesse a pasta
cd "api de sistema bancario da dio"

# 2. Copie o arquivo .env
Copy-Item .env.example .env

# 3. Inicie Docker
docker-compose up -d

# 4. Abra no navegador
# http://localhost:8000/docs
```

#### Mac/Linux
```bash
# 1. Acesse a pasta
cd "api de sistema bancario da dio"

# 2. Copie o arquivo .env
cp .env.example .env

# 3. Inicie Docker
docker-compose up -d

# 4. Abra no navegador
# http://localhost:8000/docs
```

#### Usando Script de Setup

**Windows:**
```cmd
scripts\docker-setup.bat
```

**Mac/Linux:**
```bash
bash scripts/docker-setup.sh
```

---

## 🎯 Primeiros Passos

### 1. Abra a Documentação Interativa
```
http://localhost:8000/docs
```

### 2. Registre um Usuário

Na interface Swagger:

**Clique em:** `POST /auth/register`

**Preencha com:**
```json
{
  "username": "seu_usuario",
  "password": "sua_senha"
}
```

**Clique em:** Try it out → Execute

### 3. Faça Login

**Clique em:** `POST /auth/login`

**Preencha com:**
```json
{
  "username": "seu_usuario",
  "password": "sua_senha"
}
```

**Copie o token retornado!**

### 4. Configure o Token no Swagger

**Clique no botão:** 🔒 Authorize

**Cole seu token** (sem "Bearer"):
```
seu_token_aqui
```

### 5. Crie um Cliente

**Clique em:** `POST /banco/clientes/`

**Preencha com:**
```json
{
  "nome": "João da Silva",
  "cpf": "12345678901",
  "endereco": "Rua das Flores, 123",
  "data_nascimento": "1990-05-15"
}
```

### 6. Crie uma Conta

**Clique em:** `POST /banco/contas/`

**Preencha com:**
```json
{
  "numero": 123456,
  "cpf": "12345678901"
}
```

### 7. Faça um Depósito

**Clique em:** `POST /banco/transacoes/`

**Preencha com:**
```json
{
  "numero_conta": 123456,
  "tipo_de_transacao": "deposito",
  "valor": 1000.00
}
```

### 8. Consulte sua Conta

**Clique em:** `GET /banco/contas/{numero}`

**Substitua `{numero}` por:** `123456`

Pronto! 🎉 Sua conta tem saldo!

---

## 📚 Comandos Úteis com Docker

```bash
# Ver status dos serviços
docker-compose ps

# Ver logs em tempo real
docker-compose logs -f api

# Rodar testes
docker-compose exec api pytest -v

# Acessar terminal do container
docker-compose exec api bash

# Acessar banco de dados
docker-compose exec postgres psql -U bancario -d banco_bancario

# Parar tudo
docker-compose down

# Limpar completamente
docker-compose down -v
```

---

## 📊 Serviços Disponíveis

| Serviço | URL | Credenciais |
|---------|-----|-----------|
| **API (Swagger)** | http://localhost:8000/docs | - |
| **API (ReDoc)** | http://localhost:8000/redoc | - |
| **pgAdmin** | http://localhost:5050 | admin / admin |
| **PostgreSQL** | localhost:5432 | bancario / senha123 |

---

## 🐛 Problemas Comuns

### "Port 5432 already in use"
```bash
# Mudar porta no .env
POSTGRES_PORT=5433

# Reiniciar
docker-compose restart
```

### "Cannot connect to Docker daemon"
- Inicie o Docker Desktop (Windows/Mac)
- Ou execute: `sudo systemctl start docker` (Linux)

### "Permission denied" (Linux)
```bash
# Adicionar permissão ao usuário
sudo usermod -aG docker $USER

# Logout e login novamente
```

---

## 📖 Documentação Completa

- **[README.md](README.md)** - Documentação detalhada
- **[DOCKER.md](DOCKER.md)** - Guia completo do Docker
- **[TESTES_README.md](TESTES_README.md)** - Guia de testes

---

## 🎓 Próximos Passos

1. ✅ API rodando
2. 📚 Explore as rotas em http://localhost:8000/docs
3. 🧪 Rode os testes: `docker-compose exec api pytest -v`
4. 📊 Veja dados em: http://localhost:5050 (pgAdmin)
5. 🔍 Consulte [README.md](README.md) para aprender mais

---

## 💡 Dicas

- Use **Swagger** (http://localhost:8000/docs) para testar a API
- Não precisa instalar Python se usar Docker!
- Os dados persistem mesmo depois de parar os containers
- Use pgAdmin para ver/editar dados do banco

---

**Enjoy! 🚀**
