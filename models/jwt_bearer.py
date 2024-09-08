from auth.jwt_manager import validate_token
from fastapi import HTTPException, Request, status
from fastapi.security import HTTPBearer
from jwt import DecodeError


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        if auth is None or auth.credentials is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Authorization"
            )

        try:
            data = validate_token(auth.credentials.strip("\"'"))
        except DecodeError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token"
            )

        if data["email"] != "admin@gmail.com":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials"
            )
