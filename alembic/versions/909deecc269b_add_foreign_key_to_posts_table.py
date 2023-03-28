"""Add Foreign Key to posts table

Revision ID: 909deecc269b
Revises: 46757e74e35e
Create Date: 2023-03-28 17:52:18.344170

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '909deecc269b'
down_revision = '46757e74e35e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',
                  sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk',
                          source_table='posts', referent_table='users',
                          local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
