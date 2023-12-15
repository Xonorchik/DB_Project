from sqlalchemy import Column, Integer, String, Date, ForeignKey, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from database import Base, engine


class Patient(Base):
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(150), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    policy_number = Column(Integer, nullable=False)
    social_status = Column(String(100), nullable=False)
    # 1 --> N
    treatments = relationship('Treatment', back_populates='patient')

    # 1 --> 1 for get_patient_with_medic
    medic_id = Column(Integer, ForeignKey('medics.id'))
    medic = relationship("Medic", back_populates="patients")

    # JSON поле
    search_data = Column(JSONB, nullable=True)


class Treatment(Base):
    __tablename__ = 'treatments'

    id = Column(Integer, primary_key=True, index=True)
    diagnosis = Column(String(150), nullable=False)
    current_state = Column(String(150), nullable=False)
    date_start = Column(Date, nullable=False)
    date_end = Column(Date, nullable=False)
    # N --> 1
    patient_id = Column(Integer, ForeignKey('patients.id', ondelete='CASCADE'), nullable=False)
    patient = relationship('Patient', back_populates='treatments')
    # N --> 1
    medic_id = Column(Integer, ForeignKey('medics.id', ondelete='CASCADE'), nullable=False)
    medics = relationship('Medic', secondary='treatment_medic', back_populates='treatments')


class Medic(Base):
    __tablename__ = 'medics'

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(150), nullable=False)
    speciality = Column(String(100), nullable=False)
    exp_years = Column(Integer, nullable=False)

    # 1 --> N
    treatments = relationship('Treatment', secondary='treatment_medic', back_populates='medics')

    # 1 --> 1 for get_patient_with_medic
    patients = relationship("Patient", back_populates="medic")


class TreatmentMedic(Base):
    __tablename__ = 'treatment_medic'

    treatment_id = Column(Integer, ForeignKey('treatments.id', ondelete='CASCADE'), primary_key=True)
    medic_id = Column(Integer, ForeignKey('medics.id', ondelete='CASCADE'), primary_key=True)


Index('ix_treatments_id', Treatment.id, unique=False,
      postgresql_using='gin').create(bind=engine, checkfirst=True)

Base.metadata.create_all(bind=engine)
