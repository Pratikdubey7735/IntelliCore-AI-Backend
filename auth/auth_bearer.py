from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth.auth_handler import decode_token

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            if credentials.scheme != "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme")
            try:
                payload = decode_token(credentials.credentials)
                return payload
            except Exception as e:
                raise HTTPException(status_code=403, detail=f"Invalid or expired token: {str(e)}")
        raise HTTPException(status_code=403, detail="No credentials provided")