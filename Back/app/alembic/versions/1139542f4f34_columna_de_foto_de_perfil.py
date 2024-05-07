"""columna de foto de perfil

Revision ID: 1139542f4f34
Revises: f423d6e6b40a
Create Date: 2024-04-26 12:40:29.516673

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1139542f4f34'
down_revision: Union[str, None] = 'f423d6e6b40a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('User', sa.Column('profile_picture', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('User', 'profile_picture')
    # ### end Alembic commands ###
