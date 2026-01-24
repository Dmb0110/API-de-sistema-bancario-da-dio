
'''

"""
Configuração dos testes na pasta tests2
"""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database.session import Base, get_session

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine_test = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False},
)

SessionLocalTest = sessionmaker(
    bind=engine_test,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


async def override_get_session() -> AsyncSession:
    async with SessionLocalTest() as session:
        yield session


@pytest.fixture(scope="function")
async def setup_db():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
def override_dependencies():
    app.dependency_overrides[get_session] = override_get_session


@pytest.fixture
async def client(setup_db, override_dependencies):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
'''



"""
Configuração dos testes na pasta tests2
"""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app


from app.main import app
from app.database.session import Base, get_session

# Banco de teste em memória (não afeta o banco principal)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine_test = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
)

SessionLocalTest = sessionmaker(
    bind=engine_test,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

# Override da sessão para usar o banco de teste
async def override_get_session() -> AsyncSession:
    async with SessionLocalTest() as session:
        yield session

# Cria e limpa as tabelas a cada teste
@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_db():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# Override das dependências do FastAPI
@pytest_asyncio.fixture(scope="function", autouse=True)
async def override_dependencies():
    app.dependency_overrides[get_session] = override_get_session


@pytest_asyncio.fixture
async def client(setup_db, override_dependencies):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
