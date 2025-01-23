from datetime import datetime, date

from pydantic import BaseModel, EmailStr, field_validator, ValidationError

class Patient(BaseModel):
    patient_id: int
    name: str
    phone_number: str
    email: EmailStr | None
    birth_date: date | None

class PatientCreate(BaseModel):
    name: str
    phone_number: str
    email: EmailStr | None
    birth_date: date | None
