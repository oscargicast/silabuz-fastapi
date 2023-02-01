from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer
from jwt import encode, decode
from typing import Dict


def create_token(data: Dict[int, int]) -> str:
    return encode(
        payload=data,
        key="keep-me-secret",
        algorithm="HS256",
    )


def validate_token(token: str) -> Dict[int, int]:
    return decode(
        token,
        key="keep-me-secret",
        algorithms=["HS256"],
    )


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        try:
            data = validate_token(auth.credentials)
        except Exception as _:
            raise HTTPException(status_code=403, detail="Credenciales son invalidas")
        if data['email'] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail="Credenciales son invalidas")