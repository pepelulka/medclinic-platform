from pydantic import BaseModel

class UserLogin(BaseModel):
    login: str
    password: str

class PatientUserCreate(BaseModel):
    login: str
    password: str
    patient_id: int

# Этот класс передается в jwt токене
class UserInfo(BaseModel):
    login: str
    role: str
    patient_id: int | None
