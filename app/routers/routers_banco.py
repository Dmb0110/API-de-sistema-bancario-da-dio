from fastapi import APIRouter, HTTPException, status, APIRouter, Depends

from app.schemas.schemas_do_cliente import ClienteIn, ClienteOut
from app.schemas.schemas_da_conta import ContaIn, ContaOut
from app.schemas.schemas_da_transacao import TransacaoIn, TransacaoOut, MensagemOut

from app.database.session import get_session, AsyncSession
from app.service.service_bancario import ServiceBancario
from app.autenticacao_bancaria.auth import verificar_token

router = APIRouter()


@router.get(
        "/protected"
)
async def protected_route(username: str = Depends(verificar_token)):
    return {"msg": f"Bem-vindo {username}, você acessou uma rota protegida!"}


@router.post(
        '/clientes/',
        summary="Criar cliente",
        response_model=ClienteOut,
        status_code=status.HTTP_201_CREATED
)
async def criar1(
    criar: ClienteIn,
    session: AsyncSession = Depends(get_session)
):
    cliente = await ServiceBancario.criar_cliente(criar,session)
    if cliente == 'cliente_com_esse_cpf_ja_existe':
        raise HTTPException(status_code=400,detail='Cliente com esse cpf ja existe')
    
    return cliente


@router.post(
        '/contas/',
        summary='Criar conta',
        response_model=ContaOut,
        status_code=status.HTTP_201_CREATED
)
async def criar2(
    criar: ContaIn,
    session: AsyncSession = Depends(get_session)
):
    result = await ServiceBancario.criar_conta(criar,session)
    if result ==' cliente_nao_encontrado':
        raise HTTPException(status_code=404,detail='Cliente nao encontrado')
    
    if result == 'conta_ja_existe':
        raise HTTPException(status_code=400,detail='Conta ja existe')
    # 🔑 Monta manualmente os campos extras 
    return ContaOut(
        numero=result.numero,
        agencia=result.agencia,
        saldo=result.saldo,
        titular=result.cliente.nome if result.cliente else None, 
        historico=[TransacaoOut.model_validate(t) for t in result.transacoes] if hasattr(result, "transacoes") else [] 
    )


@router.post(
        '/transacoes/',
        summary='Criar transacao',
        response_model=MensagemOut,
        status_code=status.HTTP_200_OK
)
async def criar3(
    criar: TransacaoIn,
    session: AsyncSession = Depends(get_session),
    username: str = Depends(verificar_token)
):
    result = await ServiceBancario.criar_transacao(criar,session)
    if result == 'conta_nao_encontrada':
        raise HTTPException(status_code=404,detail='Conta nao encontrada')
    
    if result == 'saldo_insuficiente':
        raise HTTPException(status_code=400,detail='Saldo insuficiente')
    
    if result == 'tipo_invalido':
        raise HTTPException(status_code=400,detail='Tipo invalido')
    
    return result


@router.get(
        '/contas/{conta}',
        summary='Consultar conta',
        response_model=ContaOut,
        status_code=status.HTTP_200_OK
)
async def consultar(
    numero: int,
    session: AsyncSession = Depends(get_session)
):
    result = await ServiceBancario.consultar_conta(numero,session)
    if result == 'conta_nao_encontrada':
        raise HTTPException(status_code=404,detail='Conta nao encontrada')
    
    return result

