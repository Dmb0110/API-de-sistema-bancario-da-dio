#!/bin/bash

# Script de Setup Docker para API de Sistema Bancário
# Uso: ./scripts/docker-setup.sh

set -e

echo "╔════════════════════════════════════════╗"
echo "║  🐳 Docker Setup - API Sistema Bancário ║"
echo "╚════════════════════════════════════════╝"
echo ""

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verificar se Docker está instalado
echo -e "${YELLOW}📋 Verificando Docker...${NC}"
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker não encontrado. Instale em: https://www.docker.com/products/docker-desktop${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Docker encontrado${NC}"

# Verificar se Docker Compose está instalado
echo -e "${YELLOW}📋 Verificando Docker Compose...${NC}"
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose não encontrado${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Docker Compose encontrado${NC}"

# Criar .env se não existir
if [ ! -f .env ]; then
    echo -e "${YELLOW}📝 Criando arquivo .env...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✅ .env criado${NC}"
else
    echo -e "${GREEN}✅ .env já existe${NC}"
fi

# Build das imagens
echo -e "${YELLOW}🔨 Construindo imagens Docker...${NC}"
docker-compose build
echo -e "${GREEN}✅ Imagens construídas${NC}"

# Iniciar serviços
echo -e "${YELLOW}🚀 Iniciando serviços...${NC}"
docker-compose up -d
echo -e "${GREEN}✅ Serviços iniciados${NC}"

# Aguardar banco ficar pronto
echo -e "${YELLOW}⏳ Aguardando PostgreSQL...${NC}"
sleep 5

# Verificar se postgres está saudável
MAX_ATTEMPTS=30
ATTEMPT=0
until docker-compose exec postgres pg_isready -U bancario > /dev/null 2>&1; do
    if [ $ATTEMPT -eq $MAX_ATTEMPTS ]; then
        echo -e "${RED}❌ PostgreSQL não respondeu após $MAX_ATTEMPTS tentativas${NC}"
        exit 1
    fi
    echo -e "${YELLOW}⏳ Tentativa $((ATTEMPT+1))/$MAX_ATTEMPTS...${NC}"
    sleep 1
    ATTEMPT=$((ATTEMPT+1))
done
echo -e "${GREEN}✅ PostgreSQL está pronto${NC}"

# Status dos containers
echo ""
echo -e "${YELLOW}📊 Status dos Containers:${NC}"
docker-compose ps

# Informações finais
echo ""
echo "╔════════════════════════════════════════╗"
echo "║        ✅ Setup Completo!              ║"
echo "╚════════════════════════════════════════╝"
echo ""
echo -e "${GREEN}🌐 Acesse os serviços em:${NC}"
echo ""
echo "  📚 Swagger (API Docs):"
echo "     http://localhost:8000/docs"
echo ""
echo "  📖 ReDoc (Documentação):"
echo "     http://localhost:8000/redoc"
echo ""
echo "  🗄️  pgAdmin (Banco de Dados):"
echo "     http://localhost:5050"
echo "     Email: admin@example.com"
echo "     Senha: admin"
echo ""
echo -e "${YELLOW}📝 Comandos úteis:${NC}"
echo ""
echo "  Ver logs:        docker-compose logs -f api"
echo "  Shell API:       docker-compose exec api bash"
echo "  Shell DB:        docker-compose exec postgres psql -U bancario -d banco_bancario"
echo "  Rodar testes:    docker-compose exec api pytest -v"
echo "  Parar serviços:  docker-compose down"
echo ""
