from fastapi import APIRouter, Request, Response
from typing import List

from pydantic import ValidationError

patients_router = APIRouter()

@patients_router.get("/api/patient/{patient_id}")
async def get_patient(req: Request, patient_id):
    result = await req.app.state.repositories['patient'].get(int(patient_id))
    return result

@patients_router.get("/api/test/auth")
async def get_test_auth(req: Request):
    if req.state.authorized:
        print(f'Authorized! ---  {req.state.user_info}')
    else:
        print(f'Not authorized')
    return "meow meow meow"
