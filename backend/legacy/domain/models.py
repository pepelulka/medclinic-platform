from datetime import datetime

from pydantic import BaseModel, EmailStr, field_validator, ValidationError

from auth.models import UserLogin


# Preview классы - классы чисто для отображения на фронтенде.
# Create классы - классы для создания объектов. Они создаются на клиенте.
# Complex классы - классы в основном для действий на фронтенде, чтобы передавать всю нужную инфу в одном объекте

# ---
# Regular classes:

class Clinic(BaseModel):
    id: int
    address: str
    name: str
    phone: str

class  Speciality(BaseModel):
    name: str

class Doctor(BaseModel):
    id: int
    name: str
    speciality: Speciality
    experience: int | None
    email: EmailStr | None
    phone_number: str

class Patient(BaseModel):
    id: int
    name: str
    phone_number: str
    email: EmailStr | None
    insurance_number: str

class Medicine(BaseModel):
    id: int
    name: str

class MedicineStock(BaseModel):
    id: int
    clinic: Clinic
    medicine: Medicine
    amount: int
    expiration_date: datetime

# ---
# Preview classes

class PatientHistoryEventPreview(BaseModel):
    doctor_name: str
    type: str
    description: str
    record_time: datetime

    @field_validator('type')
    def check_type(cls, value):
        if value in ('diagnosis', 'recovery', 'test'):
            return value
        raise ValidationError('History event type must be: "diagnosis", "recovery" or "test"')

class AppointmentPreview(BaseModel):
    id: int
    time: datetime
    doctor_name: str
    clinic_address: str

class AppointmentLogPreview(BaseModel):
    patient_id: int
    patient_name: str
    appointment_id: int
    appointment_time: datetime
    event_time: datetime
    doctor_id: int
    doctor_name: str
    clinic_address: str
    event_type: str

# ---
# Create classes

class PatientCreate(BaseModel):
    name: str
    phone_number: str
    email: EmailStr | None
    insurance_number: str

class DoctorCreate(BaseModel):
    name: str
    speciality: str
    experience: int | None
    email: EmailStr | None
    phone_number: str

class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    clinic_id: int
    time: datetime

    @field_validator('time')
    def check_time_future(cls, value):
        assert value > datetime.now()
        delta = value - datetime.now()
        assert delta.days >= 1
        return value

# ---
# Complex classes
class NewPatientWithUser(BaseModel):
    patient_info: PatientCreate
    user_login: UserLogin
