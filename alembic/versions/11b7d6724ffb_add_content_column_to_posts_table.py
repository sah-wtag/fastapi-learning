"""add content column to posts table

Revision ID: 11b7d6724ffb
Revises: 2b08f6a5afed
Create Date: 2026-09-09 16:01:52.126938

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "11b7d6724ffb"
down_revision: Union[str, Sequence[str], None] = "2b08f6a5afed"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column(
        "posts",
        "content",
    )
    pass
