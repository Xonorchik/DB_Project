from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import func, asc, desc
from sqlalchemy.orm import Session, selectinload
from models import Patient, Treatment, Medic
from database import Base, engine, SessionLocal
from pydantic import BaseModel
from datetime import date
from typing import List

from populate import session

app = FastAPI()
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class PatientCreate(BaseModel):
    full_name: str
    date_of_birth: date
    policy_number: int
    social_status: str


class PatientResponse(BaseModel):
    id: int
    full_name: str
    date_of_birth: date
    policy_number: int
    social_status: str


class PatientDelete(BaseModel):
    message: str


# Pydantic model for Result
class TreatmentCreate(BaseModel):
    diagnosis: str
    current_state: str
    date_start: date
    date_end: date
    patient_id: int
    medic_id: int


class TreatmentResponse(BaseModel):
    id: int
    diagnosis: str
    current_state: str
    date_start: date
    date_end: date
    patient_id: int
    medic_id: int


class TreatmentDelete(BaseModel):
    message: str


# Pydantic model for Athlete
class MedicCreate(BaseModel):
    full_name: str
    speciality: str
    exp_years: int


class MedicResponse(BaseModel):
    id: int
    full_name: str
    speciality: str
    exp_years: int


class MedicDelete(BaseModel):
    message: str

# Basic CRUD using FastAPI

# Create


@app.post("/patient/", response_model=PatientResponse)
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    db_patient = Patient(**patient.model_dump())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


@app.post("/treatment/", response_model=TreatmentResponse)
def create_treatment(treatment: TreatmentCreate, db: Session = Depends(get_db)):
    db_treatment = Treatment(**treatment.model_dump())
    db.add(db_treatment)
    db.commit()
    db.refresh(db_treatment)
    # for patient_with_medic
    patient = db.query(Patient).filter(Patient.id == treatment.patient_id).first() # noqa
    if patient is not None:
        patient.medic_id = treatment.medic_id
        db.commit()

    return db_treatment


@app.post("/medic/", response_model=MedicResponse)
def create_medic(medic: MedicCreate, db: Session = Depends(get_db)):
    db_medic = Medic(**medic.model_dump())
    db.add(db_medic)
    db.commit()
    db.refresh(db_medic)
    return db_medic


# Read
@app.get("/patient/{patient_id}", response_model=PatientResponse)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first() # noqa
    if patient is None:
        raise HTTPException(status_code=404, detail='Patient not found')
    return patient


@app.get("/medic/{medic_id}", response_model=MedicResponse)
def get_medic(medic_id: int, db: Session = Depends(get_db)):
    medic = db.query(Medic).filter(Medic.id == medic_id).first() # noqa
    if medic is None:
        raise HTTPException(status_code=404, detail='Medic not found')
    return medic


@app.get("/treatment/{treatment_id}", response_model=TreatmentResponse)
def get_treatment(treatment_id: int, db: Session = Depends(get_db)):
    treatment = db.query(Treatment).filter(Treatment.id == treatment_id).first() # noqa
    if treatment is None:
        raise HTTPException(status_code=404, detail='Treatment not found')
    return treatment


# Update
@app.put("/patient/{patient_id}", response_model=PatientResponse)
def update_patient(patient_id: int, updated: PatientCreate, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first() # noqa
    if patient is None:
        raise HTTPException(status_code=404, detail='Patient not found')

    for key, value in updated.model_dump().items():
        setattr(patient, key, value)

    db.commit()
    db.refresh(patient)
    return patient


@app.put("/treatment/{treatment_id}", response_model=TreatmentResponse)
def update_treatment(treatment_id: int, updated: TreatmentCreate, db: Session = Depends(get_db)):
    treatment = db.query(Treatment).filter(Treatment.id == treatment_id).first() # noqa
    if treatment is None:
        raise HTTPException(status_code=404, detail='Treatment not found')

    for key, value in updated.model_dump().items():
        setattr(treatment, key, value)

    db.commit()
    db.refresh(treatment)
    return treatment


@app.put("/medic/{medic_id}", response_model=MedicResponse)
def update_medic(medic_id: int, updated: MedicCreate, db: Session = Depends(get_db)):
    medic = db.query(Medic).filter(Medic.id == medic_id).first() # noqa
    if medic is None:
        raise HTTPException(status_code=404, detail="Medic not found")

    for key, value in updated.model_dump().items():
        setattr(medic, key, value)

    db.commit()
    db.refresh(medic)
    return medic


# Delete
@app.delete("/patient/{patient_id}", response_model=PatientDelete)
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first() # noqa
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")

    db.delete(patient)
    db.commit()
    return {"message": "Patient deleted"}


@app.delete("/treatment/{treatment_id}", response_model=TreatmentDelete)
def delete_treatment(treatment_id: int, db: Session = Depends(get_db)):
    treatment = db.query(Treatment).filter(Treatment.id == treatment_id).first() # noqa
    if treatment is None:
        raise HTTPException(status_code=404, detail="Treatment not found")

    db.delete(treatment)
    db.commit()
    return {"message": "Treatment deleted"}


@app.delete("/medic/{medic_id}", response_model=MedicDelete)
def delete_medic(medic_id: int, db: Session = Depends(get_db)):
    medic = db.query(Medic).filter(Medic.id == medic_id).first() # noqa
    if medic is None:
        raise HTTPException(status_code=404, detail="Medic not found")

    db.delete(medic)
    db.commit()
    return {"message": "Medic deleted"}


# Read with pagination
@app.get("/patient/", response_model=List[PatientResponse])
def get_patient(page: int = 0, per_page: int = 10, db: Session = Depends(get_db)):
    patient = db.query(Patient).offset(page).limit(per_page).all()
    return patient


@app.get("/treatment/", response_model=List[TreatmentResponse])
def get_treatment(page: int = 0, per_page: int = 10, db: Session = Depends(get_db)):
    treatment = db.query(Treatment).offset(page).limit(per_page).all()
    return treatment


@app.get("/medic/", response_model=List[MedicResponse])
def get_medic_sorted(page: int = 0, per_page: int = 10, sort_by: str = "id", db: Session = Depends(get_db)):
    medic = db.query(Medic).order_by(getattr(Medic, sort_by)).offset(page).limit(per_page).all()
    return medic

# SELECT... WHERE


@app.get("/api/patients/search", response_model=List[PatientResponse])
def search_patients(diagnosis: str, current_state: str, db: Session = Depends(get_db)):
    patients = db.query(Patient).filter(Treatment.diagnosis == diagnosis, # noqa
                                        Treatment.current_state == current_state).all() # noqa
    if not patients:
        raise HTTPException(status_code=404, detail="No matches found")
    return patients

# JOIN


@app.get("/api/patients_with_medic/", response_model=List[dict])
def get_patients_with_medic(db: Session = Depends(get_db)):
    patients_with_medic = db.query(Patient).options(selectinload(Patient.medic)).all()
    patients_data = []
    for patient in patients_with_medic:
        if patient.medic is not None:
            patients_data.append({
                "id": patient.id,
                "name": patient.full_name,
                "medic": {
                    "id": patient.medic.id,
                    "name": patient.medic.full_name,
                    "specialty": patient.medic.speciality,
                }
            })
    return patients_data

# UPDATE


@app.put("/api/treatments/update_by_conditions/{diagnosis}/{current_state}", response_model=TreatmentResponse)
def update_treatment_by_conditions(diagnosis: str, current_state: str, updated: TreatmentCreate,
                                   db: Session = Depends(get_db)):
    treatment = db.query(Treatment).filter(Treatment.diagnosis == diagnosis, # noqa
                                           Treatment.current_state == current_state).first() # noqa
    if treatment is None:
        raise HTTPException(status_code=404, detail='Treatment not found')

    for key, value in updated.model_dump().items():
        if updated.patient_id != 0:
            setattr(treatment, key, value)

    db.commit()
    db.refresh(treatment)
    return treatment

# GROUP BY


@app.get("/api/treatments/stats", response_model=dict)
def get_treatments_stats(db: Session = Depends(get_db)):
    result = db.query(Treatment.diagnosis,
                      func.count(Treatment.id).label('treatment_count')).group_by(Treatment.diagnosis).all()
    return {row[0]: row[1] for row in result}

# SORT


@app.get("/api/patients", response_model=List[PatientResponse])
def get_sorted_patients(sort_by: str, order: str, db: Session = Depends(get_db)):
    if order.lower() not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order parameter. Use "asc" or "desc".')

    sort_column = getattr(Patient, sort_by, None)
    if sort_column is None:
        raise HTTPException(status_code=400, detail='Invalid sort_by parameter.')

    patients_ = db.query(Patient).order_by(asc(sort_column) if order.lower() == 'asc' else desc(sort_column)).all()
    return patients_

# ORM


new_patient = Patient(full_name='John Doe', date_of_birth='1990-01-01', policy_number=123456, social_status='Active')
session.add(new_patient)
session.commit()

# READ
patients = session.query(Patient).all()
for patient in patients:
    print(patient.full_name, patient.date_of_birth)

# UPD
patient_to_update = session.query(Patient).filter_by(full_name='John Doe').first()
patient_to_update.social_status = 'Inactive'
session.commit()

# DELETE
patient_to_delete = session.query(Patient).filter_by(full_name='John Doe').first()
session.delete(patient_to_delete)
session.commit()
