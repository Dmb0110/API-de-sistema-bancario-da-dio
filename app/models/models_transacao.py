from sqlalchemy import DateTime, Integer, String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.database.session import Base

# Modelo Transacao representa movimentações financeiras ligadas a uma conta
class Transacao(Base):
    __tablename__ = "transacoes"

    # Identificador único da transação
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Tipo da transação: "deposito" ou "saque"
    tipo_de_transacao: Mapped[str] = mapped_column(String, nullable=False)

    # Valor movimentado (idealmente usar Decimal em cenários bancários reais)
    valor: Mapped[float] = mapped_column(Float, nullable=False)

    # Data/hora da transação, padrão = momento da criação
    data: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Chave estrangeira vinculando a transação a uma conta
    conta_id: Mapped[int] = mapped_column(Integer, ForeignKey("contas.id"))

    # Relacionamento: cada transação pertence a uma conta
    conta = relationship("Conta", back_populates="transacoes")
