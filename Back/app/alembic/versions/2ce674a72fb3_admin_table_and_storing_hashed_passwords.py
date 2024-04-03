"""admin table and storing hashed passwords

Revision ID: 2ce674a72fb3
Revises: 03d395be6627
Create Date: 2024-04-03 23:43:27.625890

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2ce674a72fb3"
down_revision: Union[str, None] = "03d395be6627"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "Admin",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id"], ["User.id"], name="fk_admin_user_id", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_Admin_id"), "Admin", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_Admin_id"), table_name="Admin")
    op.drop_table("Admin")
    # ### end Alembic commands ###
