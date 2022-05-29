"""create user table

Revision ID: 27e64d9d9451
Revises: 
Create Date: 2022-05-28 21:58:58.732151

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '27e64d9d9451'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("full_name", sa.String(128)),
        sa.Column("email", sa.String(128), unique=True, nullable=False),
        sa.Column("password", sa.String(128), nullable=False),
    )


def downgrade():
    op.drop_table("user")
