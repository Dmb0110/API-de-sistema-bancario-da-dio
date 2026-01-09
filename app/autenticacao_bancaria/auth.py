'''
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database.session import get_session
from app.models.models_user import User
from app.schemas.schemas_user import RegisterUsuario, LoginUsuario, UsuarioOut, TokenOut
from app.auth.auth_utils import hash_password, verify_password, create_token, verificar_token

'''
from datetime import datetime, timedelta
from jose import jwt, JWTError, ExpiredSignatureError
from passlib.context import CryptContext
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_token(sub: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": sub, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verificar_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return username
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
'''
router = APIRouter()

@router.post("/register", response_model=UsuarioOut)
async def register(data: RegisterUsuario, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).where(User.username == data.username))
    existente = result.scalars().first()
    if existente:
        raise HTTPException(status_code=400, detail="Usuário já existe")

    novo = User(username=data.username, hashed_password=hash_password(data.password))
    session.add(novo)
    await session.commit()
    await session.refresh(novo)
    return UsuarioOut.model_validate(novo)

@router.post("/login", response_model=TokenOut)
async def login(data: LoginUsuario, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).where(User.username == data.username))
    user = result.scalars().first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = create_token(sub=user.username)
    return TokenOut(access_token=token)

@router.get("/protected")
async def protected_route(username: str = Depends(verificar_token)):
    return {"msg": f"Bem-vindo {username}, você acessou uma rota protegida!"}
'''
    