from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

from db.postgres import create_connection_pool, close_connection_pool

from repositories.patient import PatientRepository

from routes.patient import patients_router

app = FastAPI()

app.include_router(patients_router)

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

@app.on_event("startup")
async def app_startup():
    app.state.conn_pool = await create_connection_pool()
    app.state.repositories = {
        "patient": PatientRepository(app.state.conn_pool)
    }


@app.on_event("shutdown")
async def app_shutdown():
    await close_connection_pool(app.state.conn_pool)
