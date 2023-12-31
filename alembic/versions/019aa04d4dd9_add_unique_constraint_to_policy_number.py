"""add_unique_constraint_to_policy_number

Revision ID: 019aa04d4dd9
Revises: 040ec3ea4f0b
Create Date: 2023-12-15 22:52:49.365984

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '019aa04d4dd9'
down_revision: Union[str, None] = '040ec3ea4f0b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('treatment_medic')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('treatment_medic',
    sa.Column('treatment_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('medic_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('treatment_id', 'medic_id', name='treatment_medic_pkey')
    )
    # ### end Alembic commands ###
