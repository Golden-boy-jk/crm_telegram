"""add fk webhook_events.bot_id -> bots.id

Revision ID: c1f3a2b4c5d6
Revises: 86027a3d177e
Create Date: 2026-01-23 18:53:47

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "c1f3a2b4c5d6"
down_revision = "86027a3d177e"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_foreign_key(
        "fk_webhook_events_bot_id_bots",
        "webhook_events",
        "bots",
        ["bot_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_webhook_events_bot_id_bots", "webhook_events", type_="foreignkey"
    )
