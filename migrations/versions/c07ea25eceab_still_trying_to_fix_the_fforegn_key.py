""" still trying to fix the fforegn key

Revision ID: c07ea25eceab
Revises: 504e9005aa7c
Create Date: 2024-07-15 15:12:04.276891

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c07ea25eceab'
down_revision = '504e9005aa7c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('card',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('suit', sa.String(length=10), nullable=False),
    sa.Column('rank', sa.String(length=10), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('game_card',
    sa.Column('game_id', sa.BigInteger(), nullable=False),
    sa.Column('card_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['card_id'], ['card.id'], ),
    sa.ForeignKeyConstraint(['game_id'], ['game.id'], ),
    sa.PrimaryKeyConstraint('game_id', 'card_id')
    )
    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.drop_constraint('game_member_id_key', type_='unique')
        batch_op.drop_column('deck')
        batch_op.drop_column('player_hand')
        batch_op.drop_column('computer_hand')
        batch_op.drop_column('tablecard')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.add_column(sa.Column('tablecard', sa.VARCHAR(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('computer_hand', sa.VARCHAR(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('player_hand', sa.VARCHAR(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('deck', sa.VARCHAR(), autoincrement=False, nullable=False))
        batch_op.create_unique_constraint('game_member_id_key', ['member_id'])

    op.drop_table('game_card')
    op.drop_table('card')
    # ### end Alembic commands ###
