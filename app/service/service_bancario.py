from sqlalchemy import select
from app.schemas.schemas_do_cliente import ClienteIn
from app.schemas.schemas_da_conta import ContaIn, ContaOut
from app.schemas.schemas_da_transacao import TransacaoOut, TransacaoIn, MensagemOut

from app.models.models_cliente import Cliente
from app.models.models_conta import Conta
from app.models.models_transacao import Transacao

from app.database.session import AsyncSession
from datetime import datetime

class ServiceBancario:
    @staticmethod
    async def criar_cliente(
        criar: ClienteIn,
        session: AsyncSession
    ) -> Cliente | str:
        
        result = await session.execute(select(Cliente).where(Cliente.cpf == criar.cpf))
        cpf = result.scalars().first()
        if cpf:
            return 'cliente_com_esse_cpf_ja_existe'
        
        novo = Cliente(**criar.model_dump())
        session.add(novo)
        await session.commit()
        await session.refresh(novo)
        return novo


    @staticmethod
    async def criar_conta(
        criar: ContaIn,
        session: AsyncSession
    ) -> Conta | str:
        
        result = await session.execute(select(Cliente).where(Cliente.cpf == criar.cpf))
        cliente = result.scalars().first()
        if not cliente:
            return 'cliente_nao_econtrado'
        
        result = await session.execute(select(Conta).where(Conta.numero == criar.numero))
        conta_existe = result.scalars().first()
        if conta_existe:
            return 'conta_ja_existe'
        
        nova = Conta(
            numero=criar.numero,
            cliente_id=cliente.id,
            saldo=0.0,
            agencia='0001'
        )
        session.add(nova)
        await session.commit()
        await session.refresh(nova)
        return nova
    
    @staticmethod
    async def consultar_conta(
        numero: int,
        session: AsyncSession
    ) -> Conta | str:
        
        result = await session.execute(select(Conta).where(Conta.numero == numero))
        conta_especifica = result.scalars().first()
        
        if not conta_especifica:
            return 'conta_nao_encontrada'
        
        return ContaOut(
        numero=conta_especifica.numero,
        agencia=conta_especifica.agencia,
        saldo=conta_especifica.saldo,
        titular=conta_especifica.cliente.nome,
        historico=[
            TransacaoOut(tipo_de_transacao=t.tipo_de_transacao, valor=t.valor, data=t.data.strftime("%d-%m-%Y %H:%M:%S"))
            for t in conta_especifica.transacoes
        ]
    )


    @staticmethod
    async def criar_transacao(
        transacao: TransacaoIn,
        session: AsyncSession
    ) -> MensagemOut:
    
        result = await session.execute(
            select(Conta).where(Conta.numero == transacao.numero_conta)
        )
        conta = result.scalars().first()
        if not conta:
            return 'conta_nao_encontrada'
       
        if transacao.tipo_de_transacao == "deposito":
            conta.saldo += transacao.valor
        elif transacao.tipo_de_transacao == "saque":
            if conta.saldo < transacao.valor:
                return 'Saldo insuficiente'
            
            conta.saldo -= transacao.valor
        else:
            return 'tipo_invalido'
    
        nova_transacao = Transacao(
            tipo_de_transacao=transacao.tipo_de_transacao,
            valor=transacao.valor,
            conta_id=conta.id,
            data=datetime.utcnow()
        )
        session.add(nova_transacao)
        await session.commit()
        await session.refresh(nova_transacao)

        return MensagemOut(mensagem=f"{transacao.tipo_de_transacao.capitalize()} realizado com sucesso")

        #return TransacaoOut.model_validate(nova_transacao)

'''
    @staticmethod
    async def criar_transacao(
        transacao: TransacaoIn,
        session: AsyncSession
    ) -> Transacao | str:
        
        result = await session.execute(select(Conta).where(Conta.numero == transacao.numero_conta))
        conta = result.scalars().first()
        if not conta:
            return 'conta_nao_encontrada'
        
        if transacao.tipo_de_transacao == 'deposito':
            conta.saldo += transacao.valor

        elif transacao.tipo_de_transacao == 'saque':
            if conta.saldo < transacao.valor:
                return 'Saldo insuficiente'
            
            conta.saldo -= transacao.valor
        else:
            return 'tipo invalido'
        
        nova_transacao = Transacao(
        tipo_de_transacao=transacao.tipo_de_transacao,
        valor=transacao.valor, conta_id=conta.id
        )
        session.add(nova_transacao)
        await session.commit()
        
        return {"mensagem": f"{transacao.tipo_de_transacao.capitalize()} realizado com sucesso"}


    @staticmethod
    async def criar_transacao(
        transacao: TransacaoIn,
        session: AsyncSession
    ) -> MensagemOut:
    
        result = await session.execute(
            select(Conta).where(Conta.numero == transacao.numero_conta)
        )
        conta = result.scalars().first()
        if not conta:
            return 'conta_nao_encontrada'
       
        if transacao.tipo_de_transacao == "deposito":
            conta.saldo += transacao.valor
        elif transacao.tipo_de_transacao == "saque":
            if conta.saldo < transacao.valor:
                return 'Saldo insuficiente'
            
            conta.saldo -= transacao.valor
        else:
            return 'tipo_invalido'
    
        nova_transacao = Transacao(
            tipo_de_transacao=transacao.tipo_de_transacao,
            valor=transacao.valor,
            conta_id=conta.id,
            data=datetime.utcnow()
        )
        session.add(nova_transacao)
        await session.commit()
        await session.refresh(nova_transacao)

        return MensagemOut(mensagem=f"{transacao.tipo_de_transacao.capitalize()} realizado com sucesso")

        #return TransacaoOut.model_validate(nova_transacao)
'''
