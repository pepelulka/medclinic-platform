from fastapi import Response
from starlette.responses import JSONResponse

# Разные типичные ответы сервера:

class ResponseTemplate:
    @staticmethod
    def error(description: str):
        return JSONResponse(
        {
            "status": "error",
            "description": description
        },
        status_code=500)

    @staticmethod
    def ok():
        return {
            "status": "ok"
        }

    @staticmethod
    def permission_denied():
        return JSONResponse(
        {
            "status": "error",
            "description": "Permission denied"
        },
        status_code=403)
