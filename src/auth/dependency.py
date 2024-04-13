import logging

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from utils import JWTEncoder, UserTokenData

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(access_token: str = Depends(oauth2_scheme)) -> UserTokenData:
    # TODO: verify token
    try:
        return JWTEncoder.decode_access_token(access_token)
    except Exception as e:
        logging.error(e)
        raise credentials_exception
