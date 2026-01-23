# 📋 Checklist Profissional - O Que Falta Pro Projeto Ficar 100%

## 🎯 Status Atual

✅ **Já tem:**
- FastAPI setup
- Docker completo
- Autenticação JWT
- Database com PostgreSQL
- Testes básicos
- Documentação
- 10 rotas funcionais

❌ **Precisa:**
- 25+ melhorias para ser production-ready

---

## 🔥 CRÍTICO (Prioritário)

### 1. **Logging Estruturado** ⭐⭐⭐
```python
# Usar Python logging + estruturado
import logging
from pythonjsonlogger import jsonlogger

# Arquivo: app/core/logger.py
# - Logs em JSON (estruturado)
# - Diferente por ambiente (dev, prod)
# - Rastreamento de requisições (request_id)
# - Stack traces completos em erro
```
**Impacto:** Crítico para debug e monitoramento em produção

---

### 2. **Tratamento de Exceções Global** ⭐⭐⭐
```python
# Arquivo: app/core/exceptions.py
class APIException(Exception):
    def __init__(self, status_code, detail, code=None):
        self.status_code = status_code
        self.detail = detail
        self.code = code

# Em main.py
@app.exception_handler(APIException)
async def api_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.code, "detail": exc.detail}
    )
```
**Por quê:** Hoje retorna string em vez de JSON estruturado

---

### 3. **Validação de Variáveis de Ambiente** ⭐⭐⭐
```python
# Arquivo: app/core/config.py
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    DATABASE_URL: str = Field(..., description="URL banco dados")
    SECRET_KEY: str = Field(..., min_length=32)
    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, gt=0)
    
    class Config:
        env_file = ".env"

settings = Settings()  # Valida ao iniciar
```
**Impacto:** Evita erros em produção

---

### 4. **Validação de Entrada Melhorada** ⭐⭐⭐
```python
# Arquivo: app/schemas/schemas_do_cliente.py
from pydantic import BaseModel, Field, EmailStr, validator
from datetime import date

class ClienteIn(BaseModel):
    nome: str = Field(..., min_length=3, max_length=100)
    cpf: str = Field(..., regex=r'^\d{11}$', description="11 dígitos")
    email: EmailStr  # Valida email
    endereco: str = Field(..., min_length=10, max_length=200)
    data_nascimento: date = Field(..., description="YYYY-MM-DD")
    
    @validator('data_nascimento')
    def validate_age(cls, v):
        from datetime import date
        age = (date.today() - v).days / 365
        if age < 18:
            raise ValueError('Maior de idade obrigatório')
        if age > 120:
            raise ValueError('Data inválida')
        return v
    
    @validator('cpf')
    def validate_cpf(cls, v):
        # Implementar validação real de CPF
        if not is_valid_cpf(v):
            raise ValueError('CPF inválido')
        return v
```

---

### 5. **CORS Restritivo em Produção** ⭐⭐⭐
```python
# Arquivo: app/core/middleware.py
# Em main.py
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,http://localhost:5500"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,  # Especificar, não "*"
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Específicos
    allow_headers=["Content-Type", "Authorization"],
    max_age=600
)
```

---

## 🚀 IMPORTANTE (Muito Necessário)

### 6. **Rate Limiting** ⭐⭐
```bash
# pip install slowapi
```

```python
# Arquivo: app/core/rate_limit.py
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)

@app.post("/auth/login")
@limiter.limit("5/minute")  # 5 tentativas por minuto
async def login(...):
    pass

@app.post("/banco/transacoes/")
@limiter.limit("10/minute")  # 10 transações por minuto
async def criar_transacao(...):
    pass
```

---

### 7. **Caching com Redis (Opcional mas Recomendado)** ⭐⭐
```bash
# docker compose: adicionar Redis
# pip install redis aioredis
```

```python
# Cache resultados de GET
from fastapi_cache2 import FastAPICache2
from fastapi_cache2.backends.redis import RedisBackend

@app.get("/get/clientes", cache=300)  # 5 minutos
async def listar_clientes(...):
    pass
```

---

### 8. **API Versioning** ⭐⭐
```python
# Estrutura:
api/
├── v1/
│   ├── clientes.py
│   ├── contas.py
│   └── transacoes.py
└── v2/
    └── ...

# Em main.py
api_v1_router = APIRouter(prefix="/api/v1")
app.include_router(api_v1_router)

# Sem quebrar clientes antigos
```

---

### 9. **Soft Deletes (Exclusão Lógica)** ⭐⭐
```python
# Em models
class Cliente(Base):
    __tablename__ = "clientes"
    
    id: int = Column(Integer, primary_key=True)
    nome: str = Column(String)
    deleted_at: datetime = Column(DateTime, nullable=True)
    
    # Query automática
    @classmethod
    def query_active(cls):
        return select(cls).where(cls.deleted_at.is_(None))

# Nunca deleta, só marca deleted_at
```

---

### 10. **Audit Logs (Rastreamento de Mudanças)** ⭐⭐
```python
# Arquivo: app/models/models_audit.py
class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id: int = Column(Integer, primary_key=True)
    entity: str = Column(String)  # "cliente", "conta", etc
    action: str = Column(String)  # "CREATE", "UPDATE", "DELETE"
    entity_id: int = Column(Integer)
    user_id: int = Column(Integer)
    old_values: dict = Column(JSON, nullable=True)
    new_values: dict = Column(JSON)
    timestamp: datetime = Column(DateTime, default=datetime.utcnow)
```

**Exemplo de uso:**
```python
# Ao criar cliente
await ServiceBancario.criar_cliente(...)
await AuditService.log_action(
    entity="cliente",
    action="CREATE",
    entity_id=cliente.id,
    new_values=cliente.dict()
)
```

---

## 📊 IMPORTANTE (Observabilidade)

### 11. **Health Checks Melhorados** ⭐⭐
```python
# Arquivo: app/routers/health.py
@router.get("/health")
async def health():
    return {"status": "ok"}

@router.get("/health/ready")
async def readiness(session: AsyncSession = Depends(get_session)):
    try:
        await session.execute(select(1))
        return {"status": "ready"}
    except:
        raise HTTPException(status_code=503)

@router.get("/health/live")
async def liveness():
    return {"status": "alive"}
```

---

### 12. **Métricas (Prometheus/OpenTelemetry)** ⭐⭐
```bash
# pip install prometheus-client
```

```python
# Arquivo: app/core/metrics.py
from prometheus_client import Counter, Histogram

request_count = Counter(
    'http_requests_total', 'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

request_duration = Histogram(
    'http_request_duration_seconds', 'HTTP request duration'
)

# Em middleware
@app.middleware("http")
async def add_metrics(request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    
    request_count.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()
    
    request_duration.observe(duration)
    return response
```

---

### 13. **Request ID Tracking** ⭐⭐
```python
# Middleware que adiciona request_id em todos os logs
import uuid
from contextvars import ContextVar

request_id_var: ContextVar[str] = ContextVar('request_id')

@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    request_id_var.set(request_id)
    
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response
```

---

## 🔒 SEGURANÇA

### 14. **SQL Injection Prevention** ⭐⭐
```python
# ✅ Já está usando SQLAlchemy ORM (seguro)
# ❌ Verificar se tem alguma query raw

# ✅ Bom:
select(Cliente).where(Cliente.cpf == cpf)

# ❌ Ruim:
session.execute(f"SELECT * FROM clientes WHERE cpf = {cpf}")
```

---

### 15. **HTTPS/TLS em Produção** ⭐⭐
```yaml
# docker-compose.prod.yml
services:
  nginx:
    environment:
      - SSL_CERTIFICATE_PATH=/etc/nginx/certs/cert.pem
      - SSL_KEY_PATH=/etc/nginx/certs/key.pem
    volumes:
      - ./certs:/etc/nginx/certs:ro
```

**Gerar certificado:**
```bash
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365
```

---

### 16. **Senha Segura - Validação Melhorada** ⭐⭐
```python
# Arquivo: app/schemas/schemas_auth.py
from pydantic import BaseModel, Field, validator

class RegisterUsuario(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(
        ...,
        min_length=12,  # 12 caracteres mínimo
        description="Mínimo 12 chars, 1 maiúscula, 1 número, 1 símbolo"
    )
    
    @validator('password')
    def validate_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('Precisa de letras maiúsculas')
        if not any(c.isdigit() for c in v):
            raise ValueError('Precisa de números')
        if not any(c in '!@#$%^&*' for c in v):
            raise ValueError('Precisa de símbolos especiais')
        return v
```

---

### 17. **2FA (Two-Factor Authentication)** ⭐
```bash
# pip install pyotp qrcode
```

```python
# Arquivo: app/service/service_2fa.py
import pyotp

def generate_2fa_secret(username: str) -> str:
    secret = pyotp.random_base32()
    return secret

def verify_2fa_token(secret: str, token: str) -> bool:
    totp = pyotp.TOTP(secret)
    return totp.verify(token)
```

---

## 🗄️ DADOS

### 18. **Backup Strategy** ⭐⭐
```bash
# Arquivo: scripts/backup.sh
#!/bin/bash
BACKUP_DIR="./backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

docker-compose exec -T postgres pg_dump \
  -U bancario banco_bancario > \
  "$BACKUP_DIR/backup_$TIMESTAMP.sql"

# Guardar últimos 30 dias
find "$BACKUP_DIR" -name "backup_*.sql" -mtime +30 -delete
```

---

### 19. **Migrations com Alembic** ⭐⭐
```bash
# Já tem setup de Alembic, mas não está sendo usado

# Criar migration
alembic revision --autogenerate -m "Adicionar email em cliente"

# Aplicar
alembic upgrade head

# Volta
alembic downgrade -1
```

---

### 20. **Data Validation - Índices** ⭐
```python
# Adicionar em models para melhor performance

class Transacao(Base):
    __tablename__ = "transacoes"
    __table_args__ = (
        Index('idx_transacoes_conta_data', 'conta_id', 'data'),
    )
    
    id: int = Column(Integer, primary_key=True)
    # ... outros campos

# Já tem alguns índices em init.sql
```

---

## 🧪 QUALIDADE DE CÓDIGO

### 21. **Code Quality Tools** ⭐⭐
```bash
pip install black flake8 pylint mypy
```

```toml
# pyproject.toml
[tool.black]
line-length = 88
target-version = ['py311']

[tool.mypy]
python_version = "3.11"
strict = true
```

---

### 22. **Pre-commit Hooks** ⭐⭐
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.1.0
    hooks:
      - id: black
  
  - repo: https://github.com/PyCQA/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
  
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.0.1
    hooks:
      - id: mypy

# Instalar
pre-commit install
```

---

### 23. **Melhorar Cobertura de Testes** ⭐⭐
```bash
# Atual: ~41 testes (bom!)
# Adicionar:
# - Testes de integração
# - Testes de erro
# - Testes de edge cases

pytest --cov=app --cov-report=html
# Objetivo: >80% cobertura
```

---

## 📚 DOCUMENTAÇÃO

### 24. **OpenAPI Tags Melhorados** ⭐
```python
# Em cada rota
@router.post(
    "/clientes/",
    tags=["Clientes"],
    responses={
        201: {"description": "Cliente criado"},
        400: {"description": "CPF duplicado"},
    }
)
```

---

### 25. **Changelog/Release Notes** ⭐
```markdown
# CHANGELOG.md

## [1.0.0] - 2026-01-12
### Added
- API de sistema bancário completa
- Docker setup
- Autenticação JWT
- Testes unitários

### Fixed
- Bug em consulta de contas

### Changed
- Melhorado tratamento de erros
```

---

## 🚀 DEPLOYMENT

### 26. **CI/CD Pipeline (GitHub Actions)** ⭐⭐
```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
    
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest --cov=app
```

---

### 27. **Environment-specific Config** ⭐⭐
```python
# Arquivo: app/core/config.py
from enum import Enum

class Environment(str, Enum):
    DEV = "dev"
    STAGING = "staging"
    PROD = "prod"

class Settings(BaseSettings):
    ENVIRONMENT: Environment = Field(default="dev")
    DEBUG: bool = Field(default=False)
    
    # Diferente por ambiente
    LOG_LEVEL: str = Field(default="INFO")
    
    class Config:
        env_file = f".env.{ENVIRONMENT}"
```

---

## 📈 MELHORIAS DE PERFORMANCE

### 28. **Compressão de Resposta** ⭐
```python
from fastapi.middleware.gzip import GZIPMiddleware

app.add_middleware(GZIPMiddleware, minimum_size=1000)
```

---

### 29. **Connection Pooling Otimizado** ⭐
```python
# Arquivo: app/database/session.py
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True,
    pool_recycle=3600
)
```

---

## 📱 EXTRAS

### 30. **GraphQL (Opcional)** ⭐
```bash
# pip install strawberry-graphql
# Para queries mais complexas
```

---

### 31. **WebSocket Support (Notificações)** ⭐
```python
# Quando novo cliente é criado, notificar
from fastapi import WebSocket

@app.websocket("/ws/clientes")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    # ... stream de atualizações
```

---

### 32. **Email/SMS Notifications** ⭐
```bash
pip install python-multipart aiosmtplib
```

```python
# Enviar email ao criar conta
async def send_email(email: str, subject: str, body: str):
    # Usar Celery para async tasks
    pass
```

---

## 📊 Prioridade Recomendada

### FASE 1 - Crítico (Faz Hoje)
1. ✅ Logging estruturado
2. ✅ Tratamento de exceções global
3. ✅ Validação de env vars
4. ✅ Validação de entrada melhorada
5. ✅ CORS restritivo

### FASE 2 - Importante (Próximas 2 semanas)
6. Rate limiting
7. Soft deletes
8. Audit logs
9. Health checks
10. Request ID tracking

### FASE 3 - Qualidade (Próximos 30 dias)
11. Métricas/Prometheus
12. Code quality tools
13. Pre-commit hooks
14. Melhorar testes
15. CI/CD

### FASE 4 - Production (Antes de Deploy)
16. HTTPS/TLS
17. 2FA
18. Backup strategy
19. Environment-specific config
20. Documentação completa

### FASE 5 - Nice to Have (Futuro)
21. Caching Redis
22. API Versioning
23. GraphQL
24. WebSocket
25. Notificações

---

## 📦 Tempo Estimado

| Fase | Tempo | Dificuldade |
|------|-------|-------------|
| 1 | 8 horas | Fácil ⭐ |
| 2 | 16 horas | Fácil-Médio ⭐⭐ |
| 3 | 12 horas | Médio ⭐⭐ |
| 4 | 8 horas | Médio ⭐⭐ |
| 5 | 20+ horas | Variável ⭐⭐⭐ |

**Total Fase 1-4: ~44 horas = ~1 semana full-time**

---

## ✅ Checklist de Deploy

- [ ] Logging estruturado implementado
- [ ] Exceptions tratadas globalmente
- [ ] Environment vars validadas
- [ ] CORS restritivo
- [ ] Rate limiting ativo
- [ ] Soft deletes implementados
- [ ] Audit logs em produção
- [ ] Health checks funcionando
- [ ] Métricas/Monitoring setup
- [ ] Testes passando (>80% cobertura)
- [ ] Code quality tools rodando
- [ ] CI/CD pipeline verde
- [ ] HTTPS/TLS configurado
- [ ] Backup strategy implementado
- [ ] Documentação completa
- [ ] CHANGELOG atualizado

---

## 🎯 Conclusão

Seu projeto está **80% pronto para produção**. Precisa principalmente de:

1. **Logging e Monitoramento** (crítico)
2. **Tratamento de erros** (crítico)
3. **Validações** (crítico)
4. **Segurança** (muito importante)
5. **CI/CD e Qualidade** (importante)

Com essas melhorias, ficará **production-ready**! 🚀
