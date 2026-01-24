from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime

# Schema de entrada para criação de transação
class TransacaoIn(BaseModel):
    numero_conta: int
    tipo_de_transacao: str
    valor: float

# Schema de saída para transação
class TransacaoOut(BaseModel):
    tipo_de_transacao: str
    valor: float
    data: str

    model_config = ConfigDict(from_attributes=True)  # permite criar a partir de objetos ORM

    # Validador para formatar a data antes de retornar
    @field_validator("data", mode="before") 
    def formatar_data(cls, v): 
        if isinstance(v, datetime): 
            return v.strftime("%d-%m-%Y %H:%M:%S") 
        return v

# Schema de saída para mensagens genéricas (ex.: confirmação de operação)
class MensagemOut(BaseModel):
    mensagem: str
