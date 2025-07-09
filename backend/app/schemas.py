# backend/app/schemas.py
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


# ----- USERS -----

class UserRead(BaseModel):
    id: UUID
    username: str
    created_at: datetime
    expires_at: datetime

    model_config = {
        "from_attributes": True
    }


class SignupResponse(UserRead):
    password_qr_uri: str
    totp_qr_uri:     str

    model_config = {"from_attributes": True}
    

# ----- AUTH & AUDIT -----
class SignupRequest(BaseModel):
    username: str


class LoginRequest(BaseModel):
    username: str
    password: str
    totp_code: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginResponse(Token):
    user: UserRead


class AuditLogRead(BaseModel):
    id: int
    user_id: UUID
    action: str
    detail: str
    timestamp: datetime

    model_config = {
        "from_attributes": True
    }
