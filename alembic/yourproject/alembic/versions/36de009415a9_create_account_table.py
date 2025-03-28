"""create account table

Revision ID: 36de009415a9
Revises: 
Create Date: 2018-08-30 12:57:31.236025

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '36de009415a9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'account',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('description', sa.Unicode(200)),
    )


def downgrade():
    op.drop_table('account')
