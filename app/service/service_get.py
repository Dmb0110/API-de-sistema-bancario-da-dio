from app.models.models_cliente import Cliente
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.database.session import AsyncSession
from app.models.models_conta import Conta
        
class ServiceGet:
    @staticmethod
    async def listar_clientes(session: AsyncSession):
        # Busca todos os clientes no banco
        result = await session.execute(select(Cliente))
        clientes = result.scalars().all()
        if not clientes:
            return 'clientes_nao_encontrados'
        return clientes
    
    @staticmethod
    async def listar_contas(session: AsyncSession):
        # Busca todas as contas no banco
        result = await session.execute(select(Conta))
        contas = result.scalars().all()
        if not contas:
            return 'contas_nao_encontradas'
        return contas
    
    @staticmethod
    async def lista_cliente_contas(cliente_id: int, session: AsyncSession):
        # Busca cliente específico e carrega suas contas associadas
        result = await session.execute(
            select(Cliente).where(Cliente.id == cliente_id)
            .options(selectinload(Cliente.contas))  # carrega contas junto com cliente
        )
        cliente = result.scalars().first()
        if not cliente:
            return 'cliente_nao_encontrado'
        return cliente
