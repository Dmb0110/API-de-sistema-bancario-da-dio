from sqlalchemy import Integer, String, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.session import Base
from typing import List

# Modelo Conta representa a tabela "contas" no banco
class Conta(Base):
    __tablename__ = "contas"

    # Identificador único da conta
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Número da conta, único e obrigatório
    numero: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)

    # Saldo da conta, inicializado em 0.0
    saldo: Mapped[float] = mapped_column(Float, default=0.0)

    # Agência da conta, padrão "0001"
    agencia: Mapped[str] = mapped_column(String, default="0001")

    # Chave estrangeira referenciando o cliente
    cliente_id: Mapped[int] = mapped_column(Integer, ForeignKey("clientes.id"))

    # Relacionamento: uma conta pertence a um cliente
    cliente = relationship("Cliente", back_populates="contas", lazy="selectin")

    # Relacionamento: uma conta pode ter várias transações
    transacoes = relationship("Transacao", back_populates="conta", lazy="selectin")

    # Propriedade para acessar o nome do titular
    @property
    def titular(self) -> str:
        return self.cliente.nome if self.cliente else None 

    # Propriedade para acessar o histórico de transações
    @property 
    def historico(self) -> List:
        return self.transacoes
