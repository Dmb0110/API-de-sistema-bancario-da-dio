from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.database.session import Base, engine
from app.rotas_principais import api_router

# Instancia a aplicação FastAPI com metadados da API
app = FastAPI(
    title="API de sistema bancário",
    description="Gerenciador de sistema bancário",
    version="1.0.0",
    docs_url="/docs",   # URL da documentação interativa Swagger
    redoc_url="/redoc"  # URL da documentação alternativa ReDoc
)

# Configura middleware de CORS para permitir requisições externas
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # aceita requisições de qualquer origem
    allow_credentials=True,
    allow_methods=["*"],  # permite todos os métodos HTTP
    allow_headers=["*"],  # permite todos os headers
)

# Evento executado na inicialização da aplicação
@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        # Cria as tabelas no banco caso não existam
        await conn.run_sync(Base.metadata.create_all)

# Inclui as rotas principais da API
app.include_router(api_router)

# Configura pasta estática "teste3" para servir arquivos (ex.: HTML, CSS, JS)
app.mount("/teste3", StaticFiles(directory=Path(__file__).parent/"teste3"), name="teste3")
