"""empty message

Revision ID: e4818770e58c
Revises: a97d67d0ce64
Create Date: 2018-05-24 14:41:25.357323

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e4818770e58c'
down_revision = 'a97d67d0ce64'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('question_result',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('result', sa.Float(), nullable=True),
    sa.Column('reversed', sa.Boolean(), nullable=True),
    sa.Column('question_number', sa.Integer(), nullable=True),
    sa.Column('question_id', sa.Integer(), nullable=True),
    sa.Column('result_scale_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['result_scale_id'], ['questionnaire_scale.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('question_result')
    # ### end Alembic commands ###
