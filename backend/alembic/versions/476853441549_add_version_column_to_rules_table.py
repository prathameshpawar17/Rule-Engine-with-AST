"""Add version column to rules table

Revision ID: 476853441549
Revises: 
Create Date: 2024-10-19 18:32:05.588371

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '476853441549'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_user_attributes_id', table_name='user_attributes')
    op.drop_index('ix_user_attributes_name', table_name='user_attributes')
    op.drop_table('user_attributes')
    op.drop_index('ix_rules_id', table_name='rules')
    op.drop_index('ix_rules_name', table_name='rules')
    op.drop_table('rules')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rules',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('ast_json', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='rules_pkey')
    )
    op.create_index('ix_rules_name', 'rules', ['name'], unique=True)
    op.create_index('ix_rules_id', 'rules', ['id'], unique=False)
    op.create_table('user_attributes',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('data_type', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='user_attributes_pkey')
    )
    op.create_index('ix_user_attributes_name', 'user_attributes', ['name'], unique=True)
    op.create_index('ix_user_attributes_id', 'user_attributes', ['id'], unique=False)
    # ### end Alembic commands ###
