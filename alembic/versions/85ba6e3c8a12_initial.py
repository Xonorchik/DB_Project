"""initial

Revision ID: 85ba6e3c8a12
Revises: 
Create Date: 2023-12-14 21:25:09.035800

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '85ba6e3c8a12'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_patients_id', table_name='patients')
    op.drop_table('patient')
    op.drop_index('ix_treatments_id', table_name='treatments')
    op.drop_table('treatment_medic')
    op.drop_index('ix_medics_id', table_name='medics')
    op.drop_table('medics')
    op.drop_table('treatment')
    op.drop_table('medic')
    op.drop_table('patients')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('medic',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('medic_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('full_name', sa.VARCHAR(length=150), autoincrement=False, nullable=False),
    sa.Column('speciality', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('exp_years', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='medic_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('treatment',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('treatment_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('diagnosis', sa.VARCHAR(length=150), autoincrement=False, nullable=False),
    sa.Column('current_state', sa.VARCHAR(length=150), autoincrement=False, nullable=False),
    sa.Column('date_start', sa.DATE(), autoincrement=False, nullable=False),
    sa.Column('date_end', sa.DATE(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='treatment_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('medics',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('medics_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('full_name', sa.VARCHAR(length=150), autoincrement=False, nullable=False),
    sa.Column('speciality', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('exp_years', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='medics_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_index('ix_medics_id', 'medics', ['id'], unique=False)
    op.create_table('treatment_medic',
    sa.Column('treatment_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('medic_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['medic_id'], ['medic.id'], name='treatment_medic_medic_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['treatment_id'], ['treatment.id'], name='treatment_medic_treatment_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('treatment_id', 'medic_id', name='treatment_medic_pkey')
    )
    op.create_table('treatments',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('diagnosis', sa.VARCHAR(length=150), autoincrement=False, nullable=False),
    sa.Column('current_state', sa.VARCHAR(length=150), autoincrement=False, nullable=False),
    sa.Column('date_start', sa.DATE(), autoincrement=False, nullable=False),
    sa.Column('date_end', sa.DATE(), autoincrement=False, nullable=False),
    sa.Column('patient_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('medic_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['medic_id'], ['medics.id'], name='treatments_medic_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['patient_id'], ['patients.id'], name='treatments_patient_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='treatments_pkey')
    )
    op.create_index('ix_treatments_id', 'treatments', ['id'], unique=False)
    op.create_table('patient',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('full_name', sa.VARCHAR(length=150), autoincrement=False, nullable=False),
    sa.Column('date_of_birth', sa.DATE(), autoincrement=False, nullable=False),
    sa.Column('policy_number', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('social_status', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='patient_pkey')
    )
    op.create_table('patients',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('full_name', sa.VARCHAR(length=150), autoincrement=False, nullable=False),
    sa.Column('date_of_birth', sa.DATE(), autoincrement=False, nullable=False),
    sa.Column('policy_number', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('social_status', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='patients_pkey')
    )
    op.create_index('ix_patients_id', 'patients', ['id'], unique=False)
    # ### end Alembic commands ###
