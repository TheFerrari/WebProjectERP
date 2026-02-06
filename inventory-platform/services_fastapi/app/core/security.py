from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
from app.core.config import settings

security = HTTPBearer()

def get_current_user(creds: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(creds.credentials, settings.jwt_secret, algorithms=['HS256'])
        return payload
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')


def require_roles(*roles):
    def checker(user=Depends(get_current_user)):
        user_roles = set(user.get('roles', []))
        if not user_roles.intersection(roles):
            raise HTTPException(status_code=403, detail='Insufficient role')
        return user
    return checker
