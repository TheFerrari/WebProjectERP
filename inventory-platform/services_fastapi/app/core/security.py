from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError
from app.core.config import settings

security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.fastapi_jwt_secret, algorithms=['HS256'])
        return payload
    except JWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token') from exc


def require_roles(*roles):
    def _checker(user=Depends(get_current_user)):
        user_roles = set(user.get('roles', []))
        if not user_roles.intersection(set(roles)):
            raise HTTPException(status_code=403, detail='Forbidden')
        return user
    return _checker
