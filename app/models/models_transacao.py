from sqlalchemy import DateTime, Integer, String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base
from datetime import datetime
from app.database.session import Base

class Transacao(Base):
    __tablename__ = "transacoes"

    id: Mapped[int] = mapped_column (primary_key=True, index=True)
    tipo_de_transacao: Mapped[str] = mapped_column(String, nullable=False)   # "deposito" ou "saque"
    valor: Mapped[float] = mapped_column(Float, nullable=False)
    data: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    conta_id: Mapped[int] = mapped_column(Integer, ForeignKey("contas.id"))

    conta = relationship("Conta", back_populates="transacoes")
