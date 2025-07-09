# backend/app/deps.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from .config import settings
from .crud import get_user_by_id
from .database import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_access_token(data: dict, expires_delta=None):
    to_encode = data.copy()
    token = jwt.encode(to_encode, settings.JWT_SECRET, algorithm="HS256")
    return token


async def get_db():
    async with SessionLocal() as session:
        yield session


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_db)
):
    """
    1) Décode le JWT Bearer
    2) Extrait le user_id du champ 'sub'
    3) Charge l'utilisateur via CRUD
    4) Lève 401 si échec
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=["HS256"]
        )
        user_id: str = payload.get("sub")
        if not user_id:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await get_user_by_id(session, user_id)
    if not user:
        raise credentials_exception

    return user
