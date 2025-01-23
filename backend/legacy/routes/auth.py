import datetime

from fastapi import APIRouter, Request, Response

from auth.auth import jwt_encode

from auth.models import UserLogin, UserInfo

router = APIRouter()

# --
# API для авторизации:

@router.post('/api/login')
async def post_login(req: Request, res: Response, user: UserLogin):
    login_result: UserInfo | None = await req.app.state.auth_repo.check_user(user)
    if login_result is None:
        return Response(content='{"message": "Error"}', status_code=401)
    # Now create jwt for UserInfo
    jwt_token = jwt_encode(login_result.model_dump(mode='json'))
    expire_time = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1))
    res.set_cookie(key='access_token', value=jwt_token, httponly=True, expires=expire_time)
    if login_result.role == 'admin':
        res.set_cookie(key='patient_id', value='admin', expires=expire_time)
    elif login_result.role == 'patient':
        res.set_cookie(key='patient_id', value=str(login_result.patient_id), expires=expire_time)
    return {"message": "ok"}

@router.get('/api/logout')
async def get_logout(req: Request, res: Response):
    res.set_cookie(key='access_token', value='deleted', httponly=True)
    res.set_cookie(key='patient_id', value='deleted')
    return {"message": "ok"}
