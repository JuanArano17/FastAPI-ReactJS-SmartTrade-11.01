"""linking card to buyer

Revision ID: 11af73214744
Revises: d753c9f00baa
Create Date: 2024-03-21 22:30:32.380422

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "11af73214744"
down_revision: Union[str, None] = "d753c9f00baa"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("Card", sa.Column("id_buyer", sa.Integer(), nullable=False))
    op.create_foreign_key(None, "Card", "Buyer", ["id_buyer"], ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "Card", type_="foreignkey")
    op.drop_column("Card", "id_buyer")
    # ### end Alembic commands ###
