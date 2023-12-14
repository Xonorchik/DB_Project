from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Session
from models import Patient, Treatment, Medic, TreatmentMedic
from database import Base, engine, SessionLocal
from pydantic import BaseModel
from datetime import date
from typing import List


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
    db_patient = Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


@app.post("/treatment/", response_model=TreatmentResponse)
def create_treatment(treatment: TreatmentCreate, db: Session = Depends(get_db)):
    db_treatment = Treatment(**treatment.dict())
    db.add(db_treatment)
    db.commit()
    db.refresh(db_treatment)
    return db_treatment


@app.post("/medic/", response_model=MedicResponse)
def create_medic(medic: MedicCreate, db: Session = Depends(get_db)):
    db_medic = Medic(**medic.dict())
    db.add(db_medic)
    db.commit()
    db.refresh(db_medic)
    return db_medic


# Read
@app.get("/patient/{patient_id}", response_model=PatientResponse)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if patient is None:
        raise HTTPException(status_code=404, detail='Patient not found')
    return patient


@app.get("/medic/{medic_id}", response_model=MedicResponse)
def get_medic(medic_id: int, db: Session = Depends(get_db)):
    medic = db.query(Medic).filter(Medic.id == medic_id).first()
    if medic is None:
        raise HTTPException(status_code=404, detail='Medic not found')
    return medic


@app.get("/treatment/{treatment_id}", response_model=TreatmentResponse)
def get_treatment(treatment_id: int, db: Session = Depends(get_db)):
    treatment = db.query(Treatment).filter(Treatment.id == treatment_id).first()
    if treatment is None:
        raise HTTPException(status_code=404, detail='Treatment not found')
    return treatment


# Update
@app.put("/patient/{patient_id}", response_model=PatientResponse)
def update_patient(patient_id: int, updated: PatientCreate, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if patient is None:
        raise HTTPException(status_code=404, detail='Patient not found')

    for key, value in updated.dict().items():
        setattr(patient, key, value)

    db.commit()
    db.refresh(patient)
    return patient


@app.put("/treatment/{treatment_id}", response_model=TreatmentResponse)
def update_treatment(treatment_id: int, updated: TreatmentCreate, db: Session = Depends(get_db)):
    treatment = db.query(Treatment).filter(Treatment.id == treatment_id).first()
    if treatment is None:
        raise HTTPException(status_code=404, detail='Treatment not found')

    for key, value in updated.dict().items():
        setattr(treatment, key, value)

    db.commit()
    db.refresh(treatment)
    return treatment


@app.put("/medic/{medic_id}", response_model=MedicResponse)
def update_medic(medic_id: int, updated: MedicCreate, db: Session = Depends(get_db)):
    medic = db.query(Medic).filter(medic_id == Medic.id).first()
    if medic is None:
        raise HTTPException(status_code=404, detail="Medic not found")

    for key, value in updated.dict().items():
        setattr(medic, key, value)

    db.commit()
    db.refresh(medic)
    return medic


# Delete
@app.delete("/patient/{patient_id}", response_model=PatientDelete)
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")

    db.delete(patient)
    db.commit()
    return {"message": "Patient deleted"}


@app.delete("/treatment/{treatment_id}", response_model=TreatmentDelete)
def delete_treatment(treatment_id: int, db: Session = Depends(get_db)):
    treatment = db.query(Treatment).filter(Treatment.id == treatment_id).first()
    if treatment is None:
        raise HTTPException(status_code=404, detail="Treatment not found")

    db.delete(treatment)
    db.commit()
    return {"message": "Treatment deleted"}


@app.delete("/medic/{medic_id}", response_model=MedicDelete)
def delete_medic(medic_id: int, db: Session = Depends(get_db)):
    medic = db.query(Medic).filter(Medic.id == medic_id).first()
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
