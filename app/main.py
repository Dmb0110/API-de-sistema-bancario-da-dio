from fastapi import FastAPI
from app.database.session import Base, engine
from app.rotas_principais import api_router

app = FastAPI(
    title="API de sistema bancário",
    description="Gerenciador de sistema bancário",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Inicializa o banco de forma assíncrona
@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        # Cria as tabelas se não existirem
        await conn.run_sync(Base.metadata.create_all)

# Inclui as rotas definidas em routers_bancario
app.include_router(api_router)
