from fastapi import APIRouter, HTTPException, status, APIRouter, Depends

from app.schemas.schemas_do_cliente import ClienteIn, ClienteOut
from app.schemas.schemas_da_conta import ContaIn, ContaOut
from app.schemas.schemas_da_transacao import TransacaoIn, TransacaoOut

from app.database.session import get_session, AsyncSession
from app.service.service_get import ServiceGet
from typing import List

router = APIRouter()

@router.get(
        '/clientes',
        summary="listar clientes",
        response_model=list[ClienteOut],
        status_code=status.HTTP_200_OK
)
async def listar(
    session: AsyncSession = Depends(get_session)
):
    cliente = await ServiceGet.listar_clientes(session)
    if cliente == 'clientes_nao_encontrados':
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Clientes nao encontrados')
    
    return cliente


@router.get(
        '/contas',
        summary="listar contas",
        response_model=list[ContaOut],
        status_code=status.HTTP_200_OK
)
async def listar(
    session: AsyncSession = Depends(get_session)
):
    contas = await ServiceGet.listar_contas(session)
    if contas == 'contas_nao_encontradas':
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Contas nao encontradas')
    
    return contas

