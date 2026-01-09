from app.models.models_cliente import Cliente
from sqlalchemy import select
from app.database.session import AsyncSession
from app.models.models_conta import Conta

class ServiceGet:
    @staticmethod
    async def listar_clientes(session: AsyncSession):
        result = await session.execute(select(Cliente))
        clientes = result.scalars().all()
        if not clientes:
            return 'clientes_nao_encontrados'
        
        return clientes
    
    @staticmethod
    async def listar_contas(session: AsyncSession):
        result = await session.execute(select(Conta))
        contas = result.scalars().all()
        if not contas:
            return 'contas_nao_encontradas'
        
        return contas
