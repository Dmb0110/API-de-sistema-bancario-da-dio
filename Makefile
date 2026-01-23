.PHONY: help build up down logs test clean restart shell db-shell

help:
	@echo "🐳 Docker Commands para API de Sistema Bancário"
	@echo ""
	@echo "Gerenciar Containers:"
	@echo "  make build          - Build da imagem Docker"
	@echo "  make up             - Inicia todos os serviços"
	@echo "  make down           - Para todos os serviços"
	@echo "  make restart        - Reinicia os serviços"
	@echo "  make clean          - Remove containers, volumes e imagens"
	@echo ""
	@echo "Logs e Status:"
	@echo "  make logs           - Ver logs de todos os serviços"
	@echo "  make logs-api       - Ver logs apenas da API"
	@echo "  make logs-db        - Ver logs apenas do PostgreSQL"
	@echo "  make ps             - Status dos containers"
	@echo ""
	@echo "Executar Comandos:"
	@echo "  make shell          - Acessar shell da API"
	@echo "  make db-shell       - Acessar psql do PostgreSQL"
	@echo "  make test           - Rodar testes pytest"
	@echo "  make test-v         - Rodar testes com verbosidade"
	@echo ""
	@echo "Setup:"
	@echo "  make setup          - Setup inicial (build + up)"
	@echo "  make reset          - Reset completo (down + clean + setup)"
	@echo ""

# Build
build:
	docker-compose build

build-no-cache:
	docker-compose build --no-cache

# Iniciar/Parar
up:
	docker-compose up -d
	@echo "✅ Serviços iniciados!"
	@echo "API: http://localhost:8000/docs"
	@echo "pgAdmin: http://localhost:5050"

down:
	docker-compose down
	@echo "✅ Serviços parados"

restart:
	docker-compose restart
	@echo "✅ Serviços reiniciados"

# Logs
logs:
	docker-compose logs -f

logs-api:
	docker-compose logs -f api

logs-db:
	docker-compose logs -f postgres

ps:
	docker-compose ps

# Testes
test:
	docker-compose exec api pytest

test-v:
	docker-compose exec api pytest -v

test-coverage:
	docker-compose exec api pytest --cov=app --cov-report=html
	@echo "✅ Cobertura gerada em htmlcov/index.html"

test-specific:
	docker-compose exec api pytest tests2/ -v

# Shell
shell:
	docker-compose exec api bash

db-shell:
	docker-compose exec postgres psql -U bancario -d banco_bancario

# Limpeza
clean:
	docker-compose down -v
	docker system prune -f
	@echo "✅ Containers, volumes e imagens não utilizadas removidos"

clean-all:
	docker-compose down -v
	docker system prune -af
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "✅ Limpeza completa realizada"

# Setup
setup:
	@echo "🚀 Setup inicial..."
	make build
	make up
	@sleep 5
	@echo "✅ Setup completo!"
	@echo ""
	@echo "Próximos passos:"
	@echo "1. Abra http://localhost:8000/docs"
	@echo "2. Crie um cliente via POST /banco/clientes/"
	@echo "3. Use pgAdmin em http://localhost:5050"

reset:
	@echo "⚠️  Resetando projeto..."
	make clean
	make setup

# Utilidades
db-backup:
	docker-compose exec postgres pg_dump -U bancario banco_bancario > backup.sql
	@echo "✅ Backup realizado: backup.sql"

db-restore:
	docker-compose exec -T postgres psql -U bancario -d banco_bancario < backup.sql
	@echo "✅ Restore completo"

freeze:
	docker-compose exec api pip freeze > requirements-frozen.txt
	@echo "✅ Dependências congeladas em requirements-frozen.txt"

# Shortcuts
start: up
stop: down
restart-api:
	docker-compose restart api
	@echo "✅ API reiniciada"
