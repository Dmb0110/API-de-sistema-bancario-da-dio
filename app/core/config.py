from pydantic_settings import BaseSettings

# Classe de configuração da aplicação, carregando variáveis do .env
class Settings(BaseSettings):
    DATABASE_URL: str                # URL de conexão com o banco de dados
    SECRET_KEY: str                  # Chave secreta usada para assinar tokens JWT
    #DEBUG: bool = False              # Flag para ativar/desativar modo debug
    ALGORITHM: str = "HS256"         # Algoritmo usado para criptografia JWT
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # Tempo de expiração do token em minutos

    class Config:
        env_file = ".env"            # Arquivo de onde as variáveis serão carregadas

# Instância única de Settings que será usada em toda a aplicação
settings = Settings()
