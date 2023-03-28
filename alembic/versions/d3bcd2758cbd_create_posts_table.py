"""Create Posts Table

Revision ID: d3bcd2758cbd
Revises:
Create Date: 2023-03-28 17:12:52.752374

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd3bcd2758cbd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts',
                    sa.Column('id', sa.Integer(),
                              nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('content', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              nullable=False, server_default=sa.text('NOW()')),
                    sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))

    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
