from fastapi import APIRouter, Request, Response

from auth.models import UserLogin
from routes.base import ResponseTemplate

router = APIRouter()

@router.post('/internal/admin/create')
async def post_admin_create(req: Request, user: UserLogin):
    repo = req.app.state.auth_repo

    try:
        await repo.create_admin(user)
    except Exception as e:
        return ResponseTemplate.error(str(e))
    return ResponseTemplate.ok()
