"""add notification delivery fields

Revision ID: 20260324_0003
Revises: 20260323_0002
Create Date: 2026-03-24 00:30:00
"""

from alembic import op
import sqlalchemy as sa


revision = "20260324_0003"
down_revision = "20260323_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "notifications",
        sa.Column("channel", sa.String(length=30), nullable=False, server_default="whatsapp"),
    )
    op.add_column(
        "notifications",
        sa.Column("recipient", sa.String(length=30), nullable=True),
    )

    op.execute(
        """
        UPDATE notifications AS n
        SET recipient = u.phone_number
        FROM alerts AS a
        JOIN fields AS f ON f.id = a.field_id
        JOIN users AS u ON u.id = f.user_id
        WHERE a.id = n.alert_id
        """
    )

    op.alter_column("notifications", "channel", server_default=None)
    op.alter_column("notifications", "recipient", nullable=False)


def downgrade() -> None:
    op.drop_column("notifications", "recipient")
    op.drop_column("notifications", "channel")
