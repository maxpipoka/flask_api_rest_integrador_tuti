"""Migracion inicial

Revision ID: 3c885e5e6f64
Revises: 
Create Date: 2023-10-31 08:48:18.438229

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c885e5e6f64'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('students_tutors',
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.Column('tutor_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
    sa.ForeignKeyConstraint(['tutor_id'], ['tutors.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('students_tutors')
    # ### end Alembic commands ###
