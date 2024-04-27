"""Creating tables

Revision ID: 65e6ee5fb63d
Revises: 
Create Date: 2024-04-22 22:37:21.339233

"""
from typing import Sequence, Union
from bot.models import User, Update
from bot.utils.db import engine

# revision identifiers, used by Alembic.
revision: str = '65e6ee5fb63d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    User.metadata.create_all(bind=engine)
    Update.metadata.create_all(bind=engine)


def downgrade() -> None:
    pass
