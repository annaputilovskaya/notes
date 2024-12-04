"""add owner to note

Revision ID: 942507cb10bf
Revises: 711ee1421775
Create Date: 2024-12-04 08:28:31.004569

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "942507cb10bf"
down_revision: Union[str, None] = "711ee1421775"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("note", sa.Column("owner", sa.Integer(), nullable=True))
    op.create_foreign_key(
        "note_owner_fkey", "note", "user", ["owner"], ["id"], ondelete="CASCADE"
    )


def downgrade() -> None:
    op.drop_constraint("note_owner_fkey", "note", type_="foreignkey")
    op.drop_column("note", "owner")
