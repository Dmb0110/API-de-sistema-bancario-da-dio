from fastapi import FastAPI
from app.models.models_bancario import engine, Base
from app.routers.routers_bancario import router

app = FastAPI(
    tittle='API de sistema bancario',
    description='Gerenciador de sistema bancario',
    version='1.0.0',
    docs_url='/docs',
    redoc_url='/redoc'
)

# Isso é útil para inicializar o banco automaticamente, mas em produção é melhor usar migrations (Alembic).
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)

app.include_router(router)
