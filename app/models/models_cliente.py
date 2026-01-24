from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.session import Base

# Modelo Cliente representa a tabela "clientes" no banco de dados
class Cliente(Base):
    __tablename__ = "clientes"

    # Identificador único do cliente (chave primária)
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Nome completo do cliente (obrigatório)
    nome: Mapped[str] = mapped_column(String, nullable=False)

    # CPF único e obrigatório (não pode repetir)
    cpf: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    # Endereço do cliente
    endereco: Mapped[str] = mapped_column(String, nullable=False)

    # Data de nascimento (armazenada como string, poderia ser Date para mais robustez)
    data_nascimento: Mapped[str] = mapped_column(String, nullable=False)

    # Relacionamento: um cliente pode ter várias contas
    contas = relationship("Conta", back_populates="cliente", lazy="selectin")
