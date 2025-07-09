import uuid
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username   = Column(String(150), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)

class AuthSecret(Base):
    __tablename__ = "auth_secrets"
    user_id = Column(String(36), ForeignKey("users.id"), primary_key=True)
    password_hash = Column(String(128), nullable=False)
    secret = Column(String(32), nullable=False)
    totp_enabled = Column(Boolean, default=True)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    action = Column(String(50), nullable=False)
    detail    = Column(String(255), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())