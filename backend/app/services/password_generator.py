# backend/app/services/password_generator.py

import httpx
from app.config import settings

async def generate_password(user_id: str) -> str:
    """
    Appelle la fonction OpenFaaS 'generate_password'.
    Retourne uniquement le mot de passe brut.
    """
    gateway = str(settings.FAAS_GATEWAY).rstrip("/")
    fn_name = "generate-password"
    url = f"{gateway}/function/{fn_name}"
    auth = (settings.FAAS_USER, settings.FAAS_PASS)

    async with httpx.AsyncClient() as client:
        response = await client.post(url, auth=auth, json={"user_id": user_id})
        response.raise_for_status()
        data = response.json()

    return data["password"]
