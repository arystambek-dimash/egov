from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

import app.config as config


class JWTRepo:
    @staticmethod
    def generate_token(data: dict):
        return jwt.encode(data, config.SECRET_KEY, algorithm=config.ALGORITHM)

    @staticmethod
    def decode_token(token: str):
        try:
            return jwt.decode(token, config.SECRET_KEY, algorithms=config.ALGORITHM)
        except:
            return {}


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication sheme."
                )
            if not self.verfity_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403, detail="Invalid token or expiredd token."
                )
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verfity_jwt(self, jwt_token: str):
        is_token_valid: bool = False

        try:
            payload = jwt.decode(
                jwt_token, config.SECRET_KEY, algorithms=config.ALGORITHM
            )
        except:
            payload = None

        if payload:
            is_token_valid = True
        return is_token_valid
