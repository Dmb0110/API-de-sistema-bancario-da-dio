from sqlalchemy import Integer, String, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base
from app.database.session import Base
from typing import List

class Conta(Base):
    __tablename__ = "contas"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    numero: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    saldo: Mapped[float] = mapped_column(Float, default=0.0)
    agencia: Mapped[str] = mapped_column(String, default="0001")
    cliente_id: Mapped[int] = mapped_column(Integer, ForeignKey("clientes.id"))

    cliente = relationship("Cliente", back_populates="contas", lazy='selectin')
    transacoes = relationship("Transacao", back_populates="conta",lazy='selectin')


    @property
    def titular(self) -> str:
        return self.cliente.nome if self.cliente else None 
    
    @property 
    def historico(self) -> List:
        return self.transacoes
    