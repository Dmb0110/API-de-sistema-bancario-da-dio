from fastapi import Depends, HTTPException
from app.schemas.schemas_auth import RegisterUsuario, UsuarioOut, LoginUsuario, TokenOut
from app.database.session import AsyncSession, get_session
from app.autenticacao_bancaria.auth import hash_password, verify_password, create_token
from app.models.models_auth import User
from sqlalchemy import select

class ServiceAuth:
    @staticmethod
    async def registrar_usuario(
            data: RegisterUsuario, 
            session: AsyncSession = Depends(get_session)
        ) -> User | str:
        # Verifica se já existe usuário com o mesmo username
        result = await session.execute(select(User).where(User.username == data.username))
        existente = result.scalars().first()
        if existente:
            return 'usuario_ja_existe'

        # Cria novo usuário com senha criptografada
        novo = User(username=data.username, hashed_password=hash_password(data.password))
        session.add(novo)
        await session.commit()
        await session.refresh(novo)
        return UsuarioOut.model_validate(novo)  # retorna dados do usuário sem expor senha
    
    @staticmethod
    async def logar_usuario(
            data: LoginUsuario, 
            session: AsyncSession = Depends(get_session)
        ) -> User | str:
        # Busca usuário pelo username
        result = await session.execute(select(User).where(User.username == data.username))
        user = result.scalars().first()

        # Valida credenciais (username e senha)
        if not user or not verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Credenciais inválidas")

        # Gera token JWT para autenticação
        token = create_token(sub=user.username)
        return TokenOut(access_token=token)
