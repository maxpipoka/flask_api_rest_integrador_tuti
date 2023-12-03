"""empty message

Revision ID: 938e4e10d465
Revises: adfb44154d0b
Create Date: 2023-12-03 10:58:01.965477

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '938e4e10d465'
down_revision = 'adfb44154d0b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('students', schema=None) as batch_op:
        batch_op.drop_constraint('students_course_id_fkey', type_='foreignkey')
        batch_op.drop_column('course_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('students', schema=None) as batch_op:
        batch_op.add_column(sa.Column('course_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('students_course_id_fkey', 'courses', ['course_id'], ['id'])

    # ### end Alembic commands ###
