from fastapi import APIRouter, Request

from domain.doctor import Speciality
from auth.auth import check_auth_admin
from routes.base import ResponseTemplate

doctors_router = APIRouter()

@doctors_router.post("/api/admin/speciality/add")
async def create_speciality(req: Request, speciality: Speciality):
    if not check_auth_admin(req.state.authorized, req.state.user_info):
        return ResponseTemplate.permission_denied()
    try:
        await req.app.state.repositories['doctor'].create_speciality(speciality)
        return ResponseTemplate.ok()
    except Exception as e:
        return ResponseTemplate.error(str(e))

@doctors_router.get("/api/admin/speciality/all")
async def get_all_specialities(req: Request):
    try:
        return await req.app.state.repositories['doctor'].get_all_specialities()
    except Exception as e:
        return ResponseTemplate.error(str(e))
