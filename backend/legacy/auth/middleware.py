from fastapi import Request

from auth.auth import jwt_decode

class AuthMiddleware:
    def __init__(
            self,
    ):
        pass

    async def __call__(self, request: Request, call_next):
        jwt_token = request.cookies.get('access_token')
        patient_id = request.cookies.get('patient_id')

        need_to_set_patient_id_in_cookies: bool = False

        if jwt_token is None:
            request.state.authorized = False
            return await call_next(request)

        try:
            user_info = jwt_decode(jwt_token)
        except Exception as e:
            request.state.authorized = False
            print(2)
            return await call_next(request)

        request.state.authorized = True
        if user_info['role'] == 'patient' and int(user_info['patient_id']) != int(patient_id):
            need_to_set_patient_id_in_cookies = True

        request.state.user_info = user_info
        response = await call_next(request)
        if need_to_set_patient_id_in_cookies:
            response.set_cookie(key='patient_id', value=user_info['patient_id'])
        return response
