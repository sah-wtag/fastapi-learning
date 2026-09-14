"""add foreign key to posts table

Revision ID: c53bae75bb9a
Revises: a0490e0d0c5e
Create Date: 2026-09-09 16:23:29.975425

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c53bae75bb9a"
down_revision: Union[str, Sequence[str], None] = "a0490e0d0c5e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "post_users_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("post_usrs_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
