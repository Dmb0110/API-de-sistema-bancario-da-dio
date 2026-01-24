from fastapi import APIRouter
from app.routers.routers_registro_login import router as auth
from app.routers.routers_banco import router as banco
from app.routers.routers_get import router as get

# Cria um roteador principal para agrupar todos os módulos da API
api_router = APIRouter()

# Inclui as rotas de autenticação (registro/login) sob o prefixo /auth
api_router.include_router(auth, prefix='/auth', tags=['auth'])

# Inclui as rotas bancárias (clientes, contas, transações) sob o prefixo /banco
api_router.include_router(banco, prefix='/banco', tags=['banco'])

# Inclui as rotas de consultas (listar clientes, contas, etc.) sob o prefixo /get
api_router.include_router(get, prefix='/get', tags=['get'])
