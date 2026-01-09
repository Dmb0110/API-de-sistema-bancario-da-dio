from fastapi import APIRouter
from app.routers.routers_registro_login import router as auth
from app.routers.routers_banco import router as banco
from app.routers.routers_get import router as get

api_router = APIRouter()

api_router.include_router(auth, prefix='/auth', tags=['auth'])

api_router.include_router(banco, prefix='/banco', tags=['banco'])

api_router.include_router(get, prefix='/get', tags=['get'])
