"""Init

Revision ID: 418d8ac83ed1
Revises: 
Create Date: 2023-11-05 21:30:26.950222

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '418d8ac83ed1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('service_users',
    sa.Column('username', sa.String(length=16), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('role', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=60), nullable=True),
    sa.Column('activated', sa.Boolean(), nullable=False),
    sa.Column('banned', sa.Boolean(), nullable=False),
    sa.Column('activation_token', sa.String(length=64), nullable=True),
    sa.Column('activation_expire', sa.DateTime(), nullable=True),
    sa.Column('password_reset_token', sa.String(length=64), nullable=True),
    sa.Column('password_reset_expire', sa.DateTime(), nullable=True),
    sa.Column('last_active', sa.DateTime(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('login', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_service_users_email'), 'service_users', ['email'], unique=False)
    op.create_index(op.f('ix_service_users_role'), 'service_users', ['role'], unique=False)
    op.create_index(op.f('ix_service_users_username'), 'service_users', ['username'], unique=False)
    op.create_table('service_auth_tokens',
    sa.Column('secret', sa.String(length=64), nullable=False),
    sa.Column('expiration', sa.DateTime(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=True),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['service_users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_service_auth_tokens_secret'), 'service_auth_tokens', ['secret'], unique=True)
    op.create_table('service_email_messages',
    sa.Column('sent_time', sa.DateTime(), nullable=True),
    sa.Column('sent', sa.Boolean(), nullable=False),
    sa.Column('type', sa.String(length=32), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('content', sa.String(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=True),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['service_users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('service_user_oauth',
    sa.Column('provider', sa.String(length=255), nullable=False),
    sa.Column('last_used', sa.DateTime(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('oauth_id', sa.String(length=32), nullable=True),
    sa.Column('user_id', sa.Uuid(), nullable=True),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['service_users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('service_user_oauth')
    op.drop_table('service_email_messages')
    op.drop_index(op.f('ix_service_auth_tokens_secret'), table_name='service_auth_tokens')
    op.drop_table('service_auth_tokens')
    op.drop_index(op.f('ix_service_users_username'), table_name='service_users')
    op.drop_index(op.f('ix_service_users_role'), table_name='service_users')
    op.drop_index(op.f('ix_service_users_email'), table_name='service_users')
    op.drop_table('service_users')
    # ### end Alembic commands ###
