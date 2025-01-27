from datetime import datetime, timezone, timedelta
import tz

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

        if jwt_token is None:
            request.state.authorized = False
            return await call_next(request)

        try:
            user_info = jwt_decode(jwt_token)
        except Exception as e:
            request.state.authorized = False
            return await call_next(request)

        current_time = datetime.now().replace(tzinfo=timezone(timedelta(hours=3)))
        print(current_time)
        if datetime.strptime(user_info['expires'], JWT_TOKEN_TIMESTAMP_FORMAT) < current_time:
            request.state.authorized = False

        request.state.authorized = True
        request.state.user_info = user_info

        return await call_next(request)
