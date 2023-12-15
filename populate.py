import requests
import random
from faker import Faker
from database import Base, engine, SessionLocal
from sqlalchemy.orm import sessionmaker
from models import Patient

BASE_URL = 'http://localhost:8000/'
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
fake = Faker()


soc_stat = ['student', 'employer', 'temporarily unemployed', 'invalid', 'pensioner', 'child']
current_stat = ['moderate', 'heavy condition', 'sent to stationary', 'died', 'recovered', 'discharged']
dr_spec = ['Cardiologist', 'Neurologist', 'Orthopedic Surgeon', 'Pediatrician', 'Ophthalmologist',
           'Dermatologist', 'Gastroenterologist', 'Endocrinologist', 'Oncologist', 'Urologist',
           'Pulmonologist', 'Rheumatologist', 'Neurologist', 'Hematologist', 'Infectious Disease Specialist']


def generate_policy_number(db: Session) -> str:
    while True:
        policy_number = fake.random_int(min=100000, max=999999)
        existing_patient = db.query(Patient).filter(Patient.policy_number == policy_number).first()
        if not existing_patient:
            return policy_number


def create_patient():
    return {
        "full_name": fake.name(),
        "date_of_birth": fake.date_of_birth().strftime('%Y-%m-%d'),
        "policy_number": generate_policy_number(SessionLocal()),
        "social_status": random.choice(soc_stat)
    }


def create_treatment(patient_id):
    return {
        "diagnosis": fake.word(),
        "current_state": random.choice(current_stat),
        "date_start": fake.date_between(start_date='-30d', end_date='today').strftime('%Y-%m-%d'),
        "date_end": fake.date_between(start_date='today', end_date='+30d').strftime('%Y-%m-%d'),
        "patient_id": patient_id,
        "medic_id": random.randint(1, 100)
    }


def create_medic():
    return {
        "full_name": fake.name(),
        "speciality": random.choice(dr_spec),
        "exp_years": fake.random_int(min=1, max=20),
    }


def populate_database(num_patients):
    for _ in range(num_patients):
        patient_data = create_patient()
        response = requests.post(BASE_URL + "patient/", json=patient_data)
        patient_id = response.json().get("id")

        treatment_data = create_treatment(patient_id)
        requests.post(BASE_URL + "treatment/", json=treatment_data)


if __name__ == "__main__":
    num_medics_to_create = 100
    for i in range(num_medics_to_create):
        medic_data = create_medic()
        requests.post(BASE_URL + "medic/", json=medic_data)
    num_patients_to_create = 1000
    populate_database(num_patients_to_create)
    print('/Population completed/')
