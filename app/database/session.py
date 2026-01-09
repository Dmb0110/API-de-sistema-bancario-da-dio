from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

# Cria o engine assíncrono usando a DATABASE_URL
# Exemplo de URL: "postgresql+asyncpg://user:password@localhost/dbname"
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_pre_ping=True
)

# Cria a fábrica de sessões assíncronas
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)

# Base declarativa para os modelos ORM
Base = declarative_base()

# Dependência para injetar sessão assíncrona no FastAPI
async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session
