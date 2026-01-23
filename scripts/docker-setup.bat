@echo off
REM Script de Setup Docker para Windows
REM Uso: scripts\docker-setup.bat

setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════╗
echo ║  🐳 Docker Setup - API Sistema Bancário ║
echo ╚════════════════════════════════════════╝
echo.

REM Verificar se Docker está instalado
echo 📋 Verificando Docker...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker não encontrado. Instale em: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)
echo ✅ Docker encontrado

REM Verificar se Docker Compose está instalado
echo 📋 Verificando Docker Compose...
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose não encontrado
    pause
    exit /b 1
)
echo ✅ Docker Compose encontrado

REM Criar .env se não existir
if not exist .env (
    echo 📝 Criando arquivo .env...
    copy .env.example .env >nul
    echo ✅ .env criado
) else (
    echo ✅ .env já existe
)

REM Build das imagens
echo.
echo 🔨 Construindo imagens Docker...
docker-compose build
if errorlevel 1 (
    echo ❌ Erro ao construir imagens
    pause
    exit /b 1
)
echo ✅ Imagens construídas

REM Iniciar serviços
echo.
echo 🚀 Iniciando serviços...
docker-compose up -d
if errorlevel 1 (
    echo ❌ Erro ao iniciar serviços
    pause
    exit /b 1
)
echo ✅ Serviços iniciados

REM Aguardar banco ficar pronto
echo.
echo ⏳ Aguardando PostgreSQL...
timeout /t 5 /nobreak

REM Verificar se postgres está saudável
set ATTEMPT=0
set MAX_ATTEMPTS=30

:check_postgres
if %ATTEMPT% equ %MAX_ATTEMPTS% (
    echo ❌ PostgreSQL não respondeu
    pause
    exit /b 1
)

docker-compose exec postgres pg_isready -U bancario >nul 2>&1
if errorlevel 1 (
    set /a ATTEMPT+=1
    echo ⏳ Tentativa !ATTEMPT!/%MAX_ATTEMPTS%...
    timeout /t 1 /nobreak
    goto check_postgres
)

echo ✅ PostgreSQL está pronto

REM Status dos containers
echo.
echo 📊 Status dos Containers:
docker-compose ps

REM Informações finais
echo.
echo ╔════════════════════════════════════════╗
echo ║        ✅ Setup Completo!              ║
echo ╚════════════════════════════════════════╝
echo.
echo 🌐 Acesse os serviços em:
echo.
echo   📚 Swagger (API Docs):
echo      http://localhost:8000/docs
echo.
echo   📖 ReDoc (Documentação):
echo      http://localhost:8000/redoc
echo.
echo   🗄️  pgAdmin (Banco de Dados):
echo      http://localhost:5050
echo      Email: admin@example.com
echo      Senha: admin
echo.
echo 📝 Comandos úteis:
echo.
echo   Ver logs:        docker-compose logs -f api
echo   Shell API:       docker-compose exec api bash
echo   Shell DB:        docker-compose exec postgres psql -U bancario -d banco_bancario
echo   Rodar testes:    docker-compose exec api pytest -v
echo   Parar serviços:  docker-compose down
echo.
pause
