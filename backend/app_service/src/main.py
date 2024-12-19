from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

from auth.db import UserCredentialsRepository
from db.postgres import create_connection_pool, close_connection_pool
from repositories.repositories import DoctorRepository, PatientRepository, PatientHistoryRepository, \
    AppointmentRepository, ClinicRepository, AppointmentHistoryRepository
from routes import api, auth

from auth.middleware import AuthMiddleware

app = FastAPI()

app.include_router(api.router)
app.include_router(auth.router)

origins = [
    "http://localhost:5173",
    "http://localhost"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

auth_middleware = AuthMiddleware()
app.add_middleware(BaseHTTPMiddleware, dispatch=auth_middleware)

@app.on_event("startup")
async def app_startup():
    app.state.conn_pool = await create_connection_pool()

    # Добавляем все репозитории:
    app.state.doctors_repo = DoctorRepository(app.state.conn_pool)
    app.state.clinics_repo = ClinicRepository(app.state.conn_pool)
    app.state.patients_repo = PatientRepository(app.state.conn_pool)
    app.state.history_repo = PatientHistoryRepository(app.state.conn_pool)
    app.state.auth_repo = UserCredentialsRepository(app.state.conn_pool)
    app.state.appointments_repo = AppointmentRepository(app.state.conn_pool)
    app.state.appointments_logs_repo = AppointmentHistoryRepository(app.state.conn_pool)

@app.on_event("shutdown")
async def app_shutdown():
    await close_connection_pool(app.state.conn_pool)
