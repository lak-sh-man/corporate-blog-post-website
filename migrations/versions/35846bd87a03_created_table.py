"""created table

Revision ID: 35846bd87a03
Revises: ed6007dccc2a
Create Date: 2024-07-27 22:57:31.697937

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '35846bd87a03'
down_revision = 'ed6007dccc2a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('profile_image', sa.String(length=20), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('admin_table', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_admin_table_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_admin_table_username'), ['username'], unique=True)

    op.create_table('user_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('profile_image', sa.String(length=20), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user_table', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_table_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_table_username'), ['username'], unique=True)

    op.create_table('adminblogpost_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('title', sa.String(length=140), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['admin_table.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('userblogpost_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('title', sa.String(length=140), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user_table.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index('ix_user_email')
        batch_op.drop_index('ix_user_username')

    op.drop_table('user')
    op.drop_table('blog_post')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blog_post',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('date', sa.DATETIME(), nullable=False),
    sa.Column('title', sa.VARCHAR(length=140), nullable=False),
    sa.Column('text', sa.TEXT(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('profile_image', sa.VARCHAR(length=20), nullable=False),
    sa.Column('email', sa.VARCHAR(length=64), nullable=True),
    sa.Column('username', sa.VARCHAR(length=64), nullable=True),
    sa.Column('password_hash', sa.VARCHAR(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index('ix_user_username', ['username'], unique=1)
        batch_op.create_index('ix_user_email', ['email'], unique=1)

    op.drop_table('userblogpost_table')
    op.drop_table('adminblogpost_table')
    with op.batch_alter_table('user_table', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_table_username'))
        batch_op.drop_index(batch_op.f('ix_user_table_email'))

    op.drop_table('user_table')
    with op.batch_alter_table('admin_table', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_admin_table_username'))
        batch_op.drop_index(batch_op.f('ix_admin_table_email'))

    op.drop_table('admin_table')
    # ### end Alembic commands ###