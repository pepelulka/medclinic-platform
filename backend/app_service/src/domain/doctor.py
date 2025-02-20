from pydantic import BaseModel
from typing import List

class Speciality(BaseModel):
    name: str

class DoctorCreate(BaseModel):
    name: str
    email: str
    phone_number: str
    specialities: List[Speciality]

class DoctorCreateResult(BaseModel):
    doctor_id: int
