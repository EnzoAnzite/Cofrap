"""rename email to username

Revision ID: fab9c7d825cd
Revises: 40db1b6fa1a5
Create Date: 2025-07-07 00:22:46.098961

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'fab9c7d825cd'
down_revision: Union[str, Sequence[str], None] = '40db1b6fa1a5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # renomme la colonne `email` en `username`
    op.alter_column(
        'users',               # nom de la table
        'email',               # ancien nom de la colonne
        new_column_name='username',
        existing_type=sa.String(length=150),
        existing_nullable=False,
        existing_server_default=None
    )


def downgrade():
    # pour revenir en arrière : rename username → email
    op.alter_column(
        'users',
        'username',
        new_column_name='email',
        existing_type=sa.String(length=150),
        existing_nullable=False,
        existing_server_default=None
    )