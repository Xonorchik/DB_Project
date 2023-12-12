from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from database import Base, engine

Base = declarative_base()


class Patient(Base):
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(150), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    policy_number = Column(Integer, nullable=False)
    social_status = Column(String(100), nullable=False)
    # 1 --> N
    treatments = relationship('Treatment', back_populates='patient')


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


class TreatmentMedic(Base):
    __tablename__ = 'treatment_medic'

    treatment_id = Column(Integer, ForeignKey('treatments.id', ondelete='CASCADE'), primary_key=True)
    medic_id = Column(Integer, ForeignKey('medics.id', ondelete='CASCADE'), primary_key=True)


Base.metadata.create_all(bind=engine)
