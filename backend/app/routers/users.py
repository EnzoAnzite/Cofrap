# backend/app/routers/users.py

from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import UserRead
from app.crud import list_users
from app.deps import get_db, get_current_user

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get(
    "/me",
    response_model=UserRead,
    summary="Profil de l'utilisateur authentifié"
)
async def read_current_user(
    user=Depends(get_current_user)
):
    return user


@router.get(
    "/",
    response_model=List[UserRead],
    summary="Liste des utilisateurs (auth required)"
)
async def read_users(
    session: AsyncSession = Depends(get_db),
    _: UserRead = Depends(get_current_user)
):
    return await list_users(session)
