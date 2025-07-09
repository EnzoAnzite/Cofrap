# backend/app/services/totp_manager.py

import httpx
from typing import Tuple
import pyotp

from app.config import settings
from app.crud import get_auth_secret
from sqlalchemy.ext.asyncio import AsyncSession

async def create_totp_secret(user_id: str) -> Tuple[str, str]:
    """
    Appelle la fonction OpenFaaS 'create-totp-secret' pour générer
    un secret TOTP et un QR-code data-URI.
    """
    gateway: str = str(settings.FAAS_GATEWAY).rstrip("/")
    fn_name = "create-totp-secret"
    url = f"{gateway}/function/{fn_name}"

    auth = (settings.FAAS_USER, settings.FAAS_PASS)

    async with httpx.AsyncClient(auth=auth, timeout=10.0) as client:
        resp = await client.post(url, content=user_id)
        resp.raise_for_status()

        data = resp.json()
        return data["secret"], data["qr_uri"]


async def verify_totp_code(
    session: AsyncSession,
    user_id: str,
    code: str
) -> bool:
    """
    Récupère le secret TOTP en base via CRUD, puis vérifie le code.
    Nécessite d'injecter la session AsyncSession.
    """
    auth = await get_auth_secret(session, user_id)
    if not auth or not auth.secret:
        return False

    totp = pyotp.TOTP(auth.secret)
    return totp.verify(code, valid_window=1)
