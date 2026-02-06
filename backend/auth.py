from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
import os
from .config import settings
from .models import Task
from .schemas import TokenData


security = HTTPBearer()


def verify_token(token: str) -> TokenData:
    """
    Verify the JWT token and extract user information.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, settings.better_auth_secret, algorithms=["HS256"]
        )

        # Extract user_id from token (assuming 'sub' contains user_id)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception

        # Check if token is expired (if 'exp' claim exists)
        exp = payload.get("exp")
        if exp and datetime.fromtimestamp(exp) < datetime.utcnow():
            raise credentials_exception

        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Dependency to get the current user from the JWT token.
    """
    token = credentials.credentials
    token_data = verify_token(token)
    return token_data.user_id


def verify_user_owns_task(current_user_id: str = Depends(get_current_user), task: Task = None) -> bool:
    """
    Verify that the current user owns the specified task.
    """
    if not task:
        return False

    if current_user_id != task.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have permission to access this resource"
        )

    return True