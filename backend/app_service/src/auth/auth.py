import base64
import bcrypt
import jwt

from settings import JWT_SECRET_KEY

ALLOWED_ROLES = [
    'patient',
    'admin'
]

# Returns base64 string
def hash_password(password: str) -> str:
    hashed_bytes = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    hashed_base64 = base64.b64encode(hashed_bytes).decode('utf-8')
    return hashed_base64

def check_password(password: str, hash_base64: str) -> bool:
    hash_bytes = base64.b64decode(hash_base64.encode('utf-8'))
    return bcrypt.checkpw(password.encode('utf-8'), hash_bytes)

def jwt_encode(payload):
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')

def jwt_decode(token):
    return jwt.decode(token, JWT_SECRET_KEY, algorithms='HS256')

# Функции для проверки прав пользователя:

def sufficient_rights_only_admin(authorized_flag, user_info):
    return authorized_flag and (
        user_info['role'] == 'admin'
    )

def sufficient_rights_confidential_info(authorized_flag, user_info, patient_id):
    return sufficient_rights_only_admin(authorized_flag, user_info) or (
            authorized_flag and user_info['role'] == 'patient' and int(user_info['patient_id']) == int(patient_id)
    )
