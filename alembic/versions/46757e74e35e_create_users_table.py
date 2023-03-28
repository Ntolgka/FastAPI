"""Create users table

Revision ID: 46757e74e35e
Revises: d3bcd2758cbd
Create Date: 2023-03-28 17:36:26.114040

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '46757e74e35e'
down_revision = 'd3bcd2758cbd'
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('username', sa.String(),
                              nullable=False, unique=True),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.Column('is_active', sa.Boolean(),
                              nullable=False, server_default='true'),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )

    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
