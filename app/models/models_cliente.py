from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base
from app.database.session import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String, nullable=False)
    cpf: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    endereco: Mapped[str] = mapped_column(String, nullable=False)
    data_nascimento: Mapped[str] = mapped_column(String, nullable=False)

    contas = relationship("Conta", back_populates="cliente",lazy='selectin')
