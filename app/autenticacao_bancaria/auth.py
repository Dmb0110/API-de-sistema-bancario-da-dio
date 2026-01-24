from datetime import datetime, timedelta
from jose import jwt, JWTError, ExpiredSignatureError
from passlib.context import CryptContext
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os

# Configurações críticas de segurança: em produção, SECRET_KEY deve vir de variável de ambiente segura
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Contexto de hashing configurado com argon2 (padrão seguro e amplamente usado)
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
security = HTTPBearer()

# Hash de senha para persistência segura (não armazenar senhas em texto puro)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Verificação de senha: compara entrada do usuário com hash armazenado
def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

# Criação de JWT com expiração; incluir claims adicionais se necessário (roles, permissões)
def create_token(sub: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({"sub": sub, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)


def verificar_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # Extrai o token do header Authorization (Bearer)
    token = credentials.credentials
    try:
        # Decodifica e valida o JWT usando chave e algoritmo configurados
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            # Se não houver claim 'sub', o token é inválido
            raise HTTPException(status_code=401, detail="Token inválido")
        return username
    except ExpiredSignatureError:
        # Token expirado: força reautenticação ou uso de refresh token
        raise HTTPException(status_code=401, detail="Token expirado")
    except JWTError:
        # Qualquer outro erro de validação: token inválido ou adulterado
        raise HTTPException(status_code=401, detail="Token inválido")
