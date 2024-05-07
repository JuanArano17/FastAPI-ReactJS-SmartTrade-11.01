"""new column id_size in shopping_cart table

Revision ID: 215bae6bf3be
Revises: 8884c2b82e21
Create Date: 2024-05-04 15:01:42.144506

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '215bae6bf3be'
down_revision: Union[str, None] = '8884c2b82e21'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('InShoppingCart', sa.Column('id_size', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_cart_size_id', 'InShoppingCart', 'Size', ['id_size'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('fk_cart_size_id', 'InShoppingCart', type_='foreignkey')
    op.drop_column('InShoppingCart', 'id_size')
    # ### end Alembic commands ###
