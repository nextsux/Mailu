"""blob: add Domain.outgoing_only

Marks a domain as send-only so Postfix does not treat it as a local
delivery destination (postfix_mailbox_domain filters out these rows).

Idempotent: safe on databases that already have the column from the
pre-upstream-rebase revision of this migration.

Upgrade note for installs that were on the old blob/outgoing-domain-only
branch (alembic_version = '8b653eeb2828' before ~11 upstream migrations
had been applied):

    UPDATE alembic_version SET version_num='6b8f5e8caaa9';

then run `alembic upgrade head`. The intermediate upstream migrations
will run and this migration replays as a no-op (column already exists).

Revision ID: 8b653eeb2828
Revises: fdff7f84d363
Create Date: 2023-03-28 21:25:25.879073
"""

revision = '8b653eeb2828'
down_revision = 'fdff7f84d363'

from alembic import op
import sqlalchemy as sa


def _column_exists(table, column):
    insp = sa.inspect(op.get_context().bind)
    return any(c['name'] == column for c in insp.get_columns(table))


def upgrade():
    if not _column_exists('domain', 'outgoing_only'):
        op.add_column('domain', sa.Column('outgoing_only', sa.Boolean(), nullable=True))


def downgrade():
    if _column_exists('domain', 'outgoing_only'):
        op.drop_column('domain', 'outgoing_only')
