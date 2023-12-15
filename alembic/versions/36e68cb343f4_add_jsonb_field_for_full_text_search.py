"""Add JSONB field for full-text search

Revision ID: 36e68cb343f4
Revises: 019aa04d4dd9
Create Date: 2023-12-16 01:01:11.626111

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '36e68cb343f4'
down_revision: Union[str, None] = '019aa04d4dd9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    connection = op.get_bind()
    inspector = sa.engine.reflection.Inspector.from_engine(connection)
    if 'treatments' not in inspector.get_table_names():
        op.create_table('treatments',
                        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                        sa.Column('diagnosis', sa.String(length=150), nullable=False),
                        sa.Column('current_state', sa.String(length=150), nullable=False),
                        sa.Column('date_start', sa.Date(), nullable=False),
                        sa.Column('date_end', sa.Date(), nullable=False),
                        sa.Column('patient_id', sa.Integer(), nullable=False),
                        sa.Column('medic_id', sa.Integer(), nullable=False),
                        sa.ForeignKeyConstraint(['medic_id'], ['medics.id'], name='treatments_medic_id_fkey',
                                                ondelete='CASCADE'),
                        sa.ForeignKeyConstraint(['patient_id'], ['patients.id'], name='treatments_patient_id_fkey',
                                                ondelete='CASCADE'),
                        sa.PrimaryKeyConstraint('id', name='treatments_pkey'),
                        )
    if not op.get_bind().has_index('treatments', 'ix_treatments_id'):
        op.create_index('ix_treatments_id', 'treatments', ['id'], unique=False)
    op.drop_constraint('patients_medic_id_fkey', 'patients', type_='foreignkey')
    op.drop_table('treatment_medic')
    inspector = sa.inspect(op.get_bind())
    indexes = inspector.get_indexes('treatments')
    if 'ix_treatments_id' in [index['name'] for index in indexes]:
        op.drop_index('ix_treatments_id', table_name='treatments')
    # op.drop_table('treatments', cascade='all')
    op.drop_index('ix_medics_id', table_name='medics')
    # op.drop_table('medics', cascade='all')
    op.drop_index('ix_patients_id', table_name='patients')
    indexes = inspector.get_indexes('patients')
    if 'ix_patients_id' in [index['name'] for index in indexes]:
        op.drop_index('ix_patients_id', table_name='patients')
    op.drop_constraint('treatments_patient_id_fkey', 'treatments', type_='foreignkey')
    op.drop_table('treatments')
    op.drop_table('patients')
    op.drop_table('medics')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('patients',
                    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('patients_id_seq'::regclass)"),
                              autoincrement=True, nullable=False),
                    sa.Column('full_name', sa.VARCHAR(length=150), autoincrement=False, nullable=False),
                    sa.Column('date_of_birth', sa.DATE(), autoincrement=False, nullable=False),
                    sa.Column('policy_number', sa.INTEGER(), autoincrement=False, nullable=False),
                    sa.Column('social_status', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
                    sa.Column('medic_id', sa.INTEGER(), autoincrement=False, nullable=True),
                    sa.ForeignKeyConstraint(['medic_id'], ['medics.id'], name='patients_medic_id_fkey'),
                    sa.PrimaryKeyConstraint('id', name='patients_pkey'),
                    postgresql_ignore_search_path=False
                    )
    op.create_table('treatment_medic',
                    sa.Column('treatment_id', sa.INTEGER(), autoincrement=False, nullable=False),
                    sa.Column('medic_id', sa.INTEGER(), autoincrement=False, nullable=False),
                    sa.PrimaryKeyConstraint('treatment_id', 'medic_id', name='treatment_medic_pkey')
                    )
    op.drop_table('patients')
    op.drop_table('treatments')
    # ### end Alembic commands ###
