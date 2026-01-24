from fastapi import APIRouter, HTTPException, status, APIRouter, Depends

from app.schemas.schemas_do_cliente import ClienteIn, ClienteOut
from app.schemas.schemas_da_conta import ContaIn, ContaOut
from app.schemas.schemas_da_transacao import TransacaoIn, TransacaoOut

from app.database.session import get_session, AsyncSession
from app.service.service_get import ServiceGet
from typing import List

router = APIRouter()  # Cria o roteador para agrupar as rotas da API

# Endpoint para listar todos os clientes
@router.get(
    "/clientes",
    summary="listar clientes",
    response_model=list[ClienteOut],
    status_code=status.HTTP_200_OK
)
async def listar(session: AsyncSession = Depends(get_session)):
    cliente = await ServiceGet.listar_clientes(session)
    if cliente == "clientes_nao_encontrados":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Clientes nao encontrados")
    return cliente

# Endpoint para listar todas as contas
@router.get(
    "/contas",
    summary="listar contas",
    response_model=list[ContaOut],
    status_code=status.HTTP_200_OK
)
async def listar(session: AsyncSession = Depends(get_session)):
    contas = await ServiceGet.listar_contas(session)
    if contas == "contas_nao_encontradas":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contas nao encontradas")
    return contas

# Endpoint para exibir um cliente específico e suas contas
@router.get(
    "/cliente/{cliente_id}",
    summary="Exibe um cliente e suas contas",
    response_model=ClienteOut,
    status_code=status.HTTP_200_OK
)
async def listar(cliente_id: int, session: AsyncSession = Depends(get_session)):
    cliente = await ServiceGet.lista_cliente_contas(cliente_id, session)
    if cliente == "cliente_nao_encontrado":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente nao encontrado")
    return cliente
