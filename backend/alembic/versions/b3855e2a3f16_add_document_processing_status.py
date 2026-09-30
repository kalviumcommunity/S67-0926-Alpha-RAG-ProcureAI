"""add document processing status

Revision ID: b3855e2a3f16
Revises: a6bcdf25d0a9
Create Date: 2026-09-23 09:51:24.709355

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'b3855e2a3f16'
down_revision: Union[str, Sequence[str], None] = 'a6bcdf25d0a9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    status_enum = postgresql.ENUM(
        "uploaded",
        "processing",
        "processed",
        "failed",
        name="document_status_enum",
    )
    status_enum.create(op.get_bind(), checkfirst=True)
    op.execute(
        "UPDATE documents SET status = 'uploaded' WHERE status IS NULL"
    )
    op.alter_column('documents', 'status',
               existing_type=sa.VARCHAR(),
               type_=status_enum,
               postgresql_using="status::text::document_status_enum",
               nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    status_enum = postgresql.ENUM(
        "uploaded",
        "processing",
        "processed",
        "failed",
        name="document_status_enum",
    )
    op.alter_column('documents', 'status',
               existing_type=status_enum,
               type_=sa.VARCHAR(),
               postgresql_using="status::text::varchar",
               nullable=True)
    status_enum.drop(op.get_bind(), checkfirst=True)
