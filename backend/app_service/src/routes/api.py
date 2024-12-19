from fastapi import APIRouter, Request, Response
from typing import List

from pydantic import ValidationError

from auth.models import PatientUserCreate
from domain.models import Doctor, Clinic, PatientCreate, AppointmentCreate, NewPatientWithUser, DoctorCreate
from auth.auth import sufficient_rights_confidential_info, sufficient_rights_only_admin

router = APIRouter()

# Разные типичные ответы сервера:

def r_error(description: str):
    return {
        "status": "error",
        "description": description
    }

def r_ok():
    return {
        "status": "ok"
    }

def r_permission_denied():
    return Response(content=r_error("Permission denied"), status_code=403)

# ---
# Общее API:

@router.get("/api/doctors", response_model=List[Doctor])
async def get_all_doctors(req: Request):
    if not req.state.authorized:
        r_permission_denied()
    result = await req.app.state.doctors_repo.get_all()
    return result

@router.get("/api/clinics", response_model=List[Clinic])
async def get_all_clinics(req: Request):
    if not req.state.authorized:
        r_permission_denied()
    result = await req.app.state.clinics_repo.get_all()
    return result

@router.get("/api/specialities")
async def get_specialities(req: Request):
    if not req.state.authorized:
        return r_permission_denied()
    return await req.app.state.doctors_repo.get_all_specialities()

# ---
# API для пациентов:

@router.get("/api/patients/{patient_id}")
async def get_patient(req: Request, patient_id):
    if not sufficient_rights_confidential_info(req.state.authorized, req.state.user_info, patient_id):
        return r_permission_denied()
    result = await req.app.state.patients_repo.get([int(patient_id)])
    return result

@router.patch("/api/patients/{patient_id}")
async def patch_patient(req: Request, patient_id, patient_create: PatientCreate):
    if not sufficient_rights_confidential_info(req.state.authorized, req.state.user_info, patient_id):
        return r_permission_denied()
    try:
        await req.app.state.patients_repo.update(int(patient_id), patient_create)
        return r_ok()
    except Exception as e:
        return r_error(str(e))

# ---
# Медицинская история:

@router.get("/api/history/{patient_id}")
async def get_history(req: Request, patient_id):
    if not sufficient_rights_confidential_info(req.state.authorized, req.state.user_info, patient_id):
        return r_permission_denied()
    result = await req.app.state.history_repo.get_history_preview(int(patient_id))
    return result

# ---
# API для записей:

@router.get("/api/appointments/{patient_id}")
async def get_appointments(req: Request, patient_id):
    if not sufficient_rights_confidential_info(req.state.authorized, req.state.user_info, patient_id):
        return r_permission_denied()
    result = await req.app.state.appointments_repo.get_all_relevant_by_user(int(patient_id))
    return result

@router.post("/api/appointments/create")
async def create_appointment(req: Request, appointment: AppointmentCreate):
    if not sufficient_rights_confidential_info(req.state.authorized, req.state.user_info, appointment.patient_id):
        return r_permission_denied()
    try:
        try:
            await req.app.state.appointments_repo.create(appointment)
        except ValidationError as e:
            return r_error(e)
        return r_ok()
    except Exception as e:
        return r_error(str(e))

@router.delete("/api/appointments/delete/{appointment_id}")
async def delete_appointment(req: Request, appointment_id: int):
    owner_patient_id = await req.app.state.appointments_repo.patient_id_from_appointment_id(appointment_id)
    if owner_patient_id is None:
        return r_error("No such appointment id")
    if not sufficient_rights_confidential_info(req.state.authorized, req.state.user_info, owner_patient_id):
        return r_permission_denied()
    await req.app.state.appointments_repo.cancel(appointment_id)
    return r_ok()

# ---
# API для админа:
@router.post("/api/patients/add")
async def add_patient(req: Request, new_patient_with_user: NewPatientWithUser):
    if not sufficient_rights_only_admin(req.state.authorized, req.state.user_info):
        return r_permission_denied()
    patient_id = await req.app.state.patients_repo.create(new_patient_with_user.patient_info)
    if patient_id is None:
        return r_error("Can't create user")
    await req.app.state.auth_repo.create_patient(PatientUserCreate(
        login=new_patient_with_user.user_login.login,
        password=new_patient_with_user.user_login.password,
        patient_id=patient_id
    ))

@router.post("/api/doctors/add")
async def add_doctor(req: Request, doctor: DoctorCreate):
    if not sufficient_rights_only_admin(req.state.authorized, req.state.user_info):
        return r_permission_denied()
    await req.app.state.doctors_repo.create(doctor)

@router.get("/api/appointments_logs")
async def get_appointments_logs(req: Request, skip: int = 0, limit: int = 10):
    if not sufficient_rights_only_admin(req.state.authorized, req.state.user_info):
        return r_permission_denied()
    return {
        "logs": await req.app.state.appointments_logs_repo.get_window(skip, limit),
        "total": await req.app.state.appointments_logs_repo.get_count()
    }
