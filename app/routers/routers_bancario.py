from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.models_bancario import Cliente, Conta, Transacao 
from app.schemas.schemas_bancario import ClienteIn, ContaIn,TransacaoIn, get_session, ContaOut, TransacaoOut

router = APIRouter()

@router.post("/clientes/")
def criar_cliente(cliente: ClienteIn, session: Session = Depends(get_session)):
    if session.query(Cliente).filter_by(cpf=cliente.cpf).first():
        raise HTTPException(status_code=400, detail="Cliente já existe")
    novo = Cliente(**cliente.dict())
    session.add(novo)
    session.commit()
    session.refresh(novo)
    return {"mensagem": "Cliente criado com sucesso"}

@router.post("/contas/")
def criar_conta(conta: ContaIn, session: Session = Depends(get_session)):
    cliente = session.query(Cliente).filter_by(cpf=conta.cpf_cliente).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    if session.query(Conta).filter_by(numero=conta.numero).first():
        raise HTTPException(status_code=400, detail="Conta já existe")
    nova = Conta(numero=conta.numero, cliente_id=cliente.id)
    session.add(nova)
    session.commit()
    session.refresh(nova)
    return {"mensagem": "Conta criada com sucesso"}

@router.post("/transacoes/")
def realizar_transacao(transacao: TransacaoIn, session: Session = Depends(get_session)):
    conta = session.query(Conta).filter_by(numero=transacao.numero_conta).first()
    if not conta:
        raise HTTPException(status_code=404, detail="Conta não encontrada")

    if transacao.tipo_de_transacao.lower() == "deposito":
        conta.saldo += transacao.valor
    elif transacao.tipo_de_transacao.lower() == "saque":
        if conta.saldo < transacao.valor:
            raise HTTPException(status_code=400, detail="Saldo insuficiente")
        conta.saldo -= transacao.valor
    else:
        raise HTTPException(status_code=400, detail="Tipo inválido")

    nova_transacao = Transacao(tipo_de_transacao=transacao.tipo_de_transacao, valor=transacao.valor, conta_id=conta.id)
    session.add(nova_transacao)
    session.commit()
    return {"mensagem": f"{transacao.tipo_de_transacao.capitalize()} realizado com sucesso"}

@router.get("/contas/{numero}", response_model=ContaOut)
def consultar_conta(numero: int, session: Session = Depends(get_session)):
    conta = session.query(Conta).filter_by(numero=numero).first()
    if not conta:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    return ContaOut(
        numero=conta.numero,
        agencia=conta.agencia,
        saldo=conta.saldo,
        titular=conta.cliente.nome,
        historico=[
            TransacaoOut(tipo_de_transacao=t.tipo_de_transacao, valor=t.valor, data=t.data.strftime("%d-%m-%Y %H:%M:%S"))
            for t in conta.transacoes
        ]
    )
