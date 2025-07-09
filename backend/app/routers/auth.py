# backend/app/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
import bcrypt
from jose import jwt
from app.crud import (
    get_user_by_username,
    get_auth_secret,
    create_user,
    create_auth_secret,
    create_audit_log
)
from app.schemas import SignupRequest, SignupResponse, UserRead, LoginRequest, LoginResponse
from app.database import get_db
from app.services.password_generator import generate_password
from app.services.totp_manager import create_totp_secret, verify_totp_code
from app.config import settings
from app.services.qr_utils import generate_text_qr

router = APIRouter(tags=["auth"])

@router.post(
    "/signup",
    response_model=SignupResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Créer un nouvel utilisateur et retourner le qr de totp"
)
async def signup(
    payload: SignupRequest,
    session: AsyncSession = Depends(get_db)
):
    # 1) Pas déjà inscrit ?
    if await get_user_by_username(session, payload.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cet utilisateur est déjà pris"
        )

    # 2) Créer le User (expiry à 6 mois)
    expires = datetime.utcnow() + timedelta(days=183)
    user = await create_user(
        session,
        username=payload.username,
        expires_at=expires
    )

    # 3) Générer un mot de passe robuste via openfaas
    #    (la fonction generate_password attend user_id)
    raw_password = await generate_password(user.id)
    password_hash = bcrypt.hashpw(
        raw_password.encode(), bcrypt.gensalt()
    ).decode()
    # 4) Générer le secret TOTP et et récupérer le QR TOTP
    totp_secret, totp_qr_uri = await create_totp_secret(user.id)

    # 5) Stocker hash + secret
    await create_auth_secret(
        session,
        user_id=user.id,
        password_hash=password_hash,
        secret=totp_secret
    )
    # 6) Journaliser
    await create_audit_log(
        session,
        user_id=user.id,
        action="signup",
        detail=f"Mot de passe généré : {raw_password}"
    )
    user_data = UserRead.from_orm(user)
    # 6) Générer le QR mot de passe
    password_qr_uri = generate_text_qr(f"Mot de passe : {raw_password}")
    return SignupResponse(
        **user_data.dict(),
        password_qr_uri=password_qr_uri,
        totp_qr_uri=totp_qr_uri
    )

@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    summary="Authentifier un utilisateur et obtenir un JWT"
)
async def login(
    payload: LoginRequest,
    session: AsyncSession = Depends(get_db)
):
    user = await get_user_by_username(session, payload.username)
    if not user:
        raise HTTPException(400, "Identifiants invalides")

    auth = await get_auth_secret(session, user.id)
    if not auth or not bcrypt.checkpw(
        payload.password.encode(), auth.password_hash.encode()
    ):
        raise HTTPException(400, "Identifiants invalides")

    if auth.totp_enabled:
        if not await verify_totp_code(session, user.id, payload.totp_code):
            raise HTTPException(400, "Code TOTP invalide")

    if user.expires_at < datetime.utcnow():
        raise HTTPException(403, "Compte expiré")

    expire = datetime.utcnow() + timedelta(minutes=60)
    token = jwt.encode(
        {"sub": str(user.id), "exp": expire},
        settings.JWT_SECRET,
        algorithm="HS256"
    )

    await create_audit_log(
        session,
        user_id=user.id,
        action="login",
        detail="Connexion réussie"
    )

    return LoginResponse(access_token=token, user=user)
