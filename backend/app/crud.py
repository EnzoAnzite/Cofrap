# app/crud.py
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User, AuthSecret, AuditLog


# -------- USER --------

async def get_user_by_id(session: AsyncSession, user_id: UUID) -> Optional[User]:
    q = select(User).where(User.id == user_id)
    result = await session.execute(q)
    return result.scalars().first()

async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    q = select(User).where(User.username == username)
    result = await session.execute(q)
    return result.scalars().first()

async def list_users(session: AsyncSession, skip: int = 0, limit: int = 100) -> List[User]:
    q = select(User).offset(skip).limit(limit)
    result = await session.execute(q)
    return result.scalars().all()

async def create_user(
    session: AsyncSession, *, username: str, expires_at: datetime
) -> User:
    user = User(username=username, expires_at=expires_at)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

async def update_user_expiry(
    session: AsyncSession, *, user_id: UUID, new_expires_at: datetime
) -> None:
    q = (
        update(User)
        .where(User.id == user_id)
        .values(expires_at=new_expires_at)
    )
    await session.execute(q)
    await session.commit()


# -------- AUTH SECRET --------

async def get_auth_secret(session: AsyncSession, user_id: UUID) -> Optional[AuthSecret]:
    q = select(AuthSecret).where(AuthSecret.user_id == user_id)
    result = await session.execute(q)
    return result.scalars().first()

async def create_auth_secret(
    session: AsyncSession, *, user_id: UUID, password_hash: str, secret: str
) -> AuthSecret:
    auth = AuthSecret(
        user_id=user_id,
        password_hash=password_hash,
        secret=secret,
        totp_enabled=True,
    )
    session.add(auth)
    await session.commit()
    await session.refresh(auth)
    return auth

async def update_password_hash(
    session: AsyncSession, *, user_id: UUID, new_hash: str
) -> None:
    q = (
        update(AuthSecret)
        .where(AuthSecret.user_id == user_id)
        .values(password_hash=new_hash)
    )
    await session.execute(q)
    await session.commit()

async def disable_totp(session: AsyncSession, *, user_id: UUID) -> None:
    q = (
        update(AuthSecret)
        .where(AuthSecret.user_id == user_id)
        .values(totp_enabled=False)
    )
    await session.execute(q)
    await session.commit()


# -------- AUDIT LOG --------

async def create_audit_log(
    session: AsyncSession, *, user_id: UUID, action: str, detail: str
) -> AuditLog:
    log = AuditLog(user_id=user_id, action=action, detail=detail)
    session.add(log)
    await session.commit()
    await session.refresh(log)
    return log

async def list_audit_logs(
    session: AsyncSession, *, user_id: Optional[UUID] = None
) -> List[AuditLog]:
    q = select(AuditLog)
    if user_id:
        q = q.where(AuditLog.user_id == user_id)
    result = await session.execute(q)
    return result.scalars().all()
