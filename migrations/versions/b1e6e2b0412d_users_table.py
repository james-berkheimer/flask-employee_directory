"""users table

Revision ID: b1e6e2b0412d
Revises: 
Create Date: 2019-10-11 13:10:50.216380

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1e6e2b0412d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('employees',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('first_name', sa.String(length=64), nullable=True),
    sa.Column('last_name', sa.String(length=64), nullable=True),
    sa.Column('job_title', sa.String(length=64), nullable=True),
    sa.Column('department', sa.String(length=64), nullable=True),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.Column('current_employee', sa.Boolean(), nullable=True),
    sa.Column('image_name', sa.String(length=255), nullable=True),
    sa.Column('about_me', sa.String(length=140), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_employees_current_employee'), 'employees', ['current_employee'], unique=False)
    op.create_index(op.f('ix_employees_department'), 'employees', ['department'], unique=False)
    op.create_index(op.f('ix_employees_email'), 'employees', ['email'], unique=True)
    op.create_index(op.f('ix_employees_first_name'), 'employees', ['first_name'], unique=False)
    op.create_index(op.f('ix_employees_job_title'), 'employees', ['job_title'], unique=False)
    op.create_index(op.f('ix_employees_last_name'), 'employees', ['last_name'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_employees_last_name'), table_name='employees')
    op.drop_index(op.f('ix_employees_job_title'), table_name='employees')
    op.drop_index(op.f('ix_employees_first_name'), table_name='employees')
    op.drop_index(op.f('ix_employees_email'), table_name='employees')
    op.drop_index(op.f('ix_employees_department'), table_name='employees')
    op.drop_index(op.f('ix_employees_current_employee'), table_name='employees')
    op.drop_table('employees')
    # ### end Alembic commands ###
