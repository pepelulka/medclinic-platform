from fastapi import Response

# Разные типичные ответы сервера:

class ResponseTemplate:
    @staticmethod
    def error(description: str):
        return {
            "status": "error",
            "description": description
        }

    @staticmethod
    def ok():
        return {
            "status": "ok"
        }

    @staticmethod
    def permission_denied():
        return Response(content=ResponseTemplate.error("Permission denied"), status_code=403)
