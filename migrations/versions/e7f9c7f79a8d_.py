"""empty message

Revision ID: e7f9c7f79a8d
Revises: e2acc329e232
Create Date: 2020-07-27 11:14:31.819614

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e7f9c7f79a8d'
down_revision = 'e2acc329e232'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('photos')
    op.drop_index('ix_messages_timestamp', table_name='messages')
    op.drop_table('messages')
    op.drop_index('ix_notifications_name', table_name='notifications')
    op.drop_index('ix_notifications_timestamp', table_name='notifications')
    op.drop_table('notifications')
    op.add_column('transactionfees', sa.Column('currency_symbol', sa.String(), nullable=True))
    op.add_column('transactionfees', sa.Column('european_fee', sa.Integer(), nullable=True))
    op.add_column('transactionfees', sa.Column('european_percentage', sa.Float(), nullable=True))
    op.add_column('transactionfees', sa.Column('international_fee', sa.Integer(), nullable=True))
    op.add_column('transactionfees', sa.Column('international_percentage', sa.Float(), nullable=True))
    op.add_column('transactionfees', sa.Column('local_fee', sa.Integer(), nullable=True))
    op.add_column('transactionfees', sa.Column('local_percentage', sa.Float(), nullable=True))
    op.drop_column('transactionfees', 'provider_fee')
    op.drop_column('transactionfees', 'provider_percentage')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transactionfees', sa.Column('provider_percentage', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.add_column('transactionfees', sa.Column('provider_fee', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('transactionfees', 'local_percentage')
    op.drop_column('transactionfees', 'local_fee')
    op.drop_column('transactionfees', 'international_percentage')
    op.drop_column('transactionfees', 'international_fee')
    op.drop_column('transactionfees', 'european_percentage')
    op.drop_column('transactionfees', 'european_fee')
    op.drop_column('transactionfees', 'currency_symbol')
    op.create_table('notifications',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=128), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('related_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('timestamp', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('payload_json', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('read', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='notifications_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='notifications_pkey')
    )
    op.create_index('ix_notifications_timestamp', 'notifications', ['timestamp'], unique=False)
    op.create_index('ix_notifications_name', 'notifications', ['name'], unique=False)
    op.create_table('messages',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('recipient_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('body', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('timestamp', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('read_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['recipient_id'], ['users.id'], name='messages_recipient_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='messages_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='messages_pkey')
    )
    op.create_index('ix_messages_timestamp', 'messages', ['timestamp'], unique=False)
    op.create_table('photos',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('image_filename', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('image_url', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='photos_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='photos_pkey')
    )
    # ### end Alembic commands ###