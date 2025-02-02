from datetime import datetime, timezone, timedelta
from typing import Any

import jwt
from fastapi import Request

from settings import JWT_SECRET_KEY, JWT_TOKEN_TIMESTAMP_FORMAT

ALLOWED_ROLES = [
    'patient',
    'doctor',
    'admin'
]

def jwt_decode(token):
    return jwt.decode(token, JWT_SECRET_KEY, algorithms='HS256')

class AuthMiddleware:
    def __init__(self):
        pass

    async def __call__(self, request: Request, call_next):
        jwt_token = request.cookies.get('jwt')

        request.state.authorized = False
        request.state.user_info = None

        if jwt_token is None:
            return await call_next(request)

        try:
            user_info = jwt_decode(jwt_token)
        except Exception as e:
            return await call_next(request)

        current_time = datetime.now().replace(tzinfo=timezone(timedelta(hours=3)))
        print(current_time)
        if datetime.strptime(user_info['expires'], JWT_TOKEN_TIMESTAMP_FORMAT) < current_time:
            return await call_next(request)

        request.state.authorized = True
        request.state.user_info = user_info

        return await call_next(request)

def check_auth_admin(authorized_flag: bool, user_info: Any):
    return authorized_flag and user_info['role'] == 'admin'
