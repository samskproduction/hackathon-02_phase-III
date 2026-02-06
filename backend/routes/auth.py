from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import Dict
import jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from pydantic import BaseModel
from core.config import settings
from models.user import User, UserCreate, UserResponse
from database.database import get_session
from utils.responses import create_success_response, create_error_response

router = APIRouter(prefix="/auth", tags=["auth"])

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

from datetime import timezone

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=30)) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta  # Use timezone-aware datetime
    to_encode.update({"exp": int(expire.timestamp())})  # Convert to integer to ensure proper JWT format
    encoded_jwt = jwt.encode(to_encode, settings.BETTER_AUTH_SECRET, algorithm="HS256")
    return encoded_jwt


@router.post("/register", response_model=dict)
async def register_user(
    user_data: UserCreate,
    session: Session = Depends(get_session)
):
    """Register a new user in the database"""
    # Check if user already exists
    existing_user = session.exec(select(User).where(User.email == user_data.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=create_error_response("AUTH_004", "User with this email already exists", 400)
        )

    # Create new user with hashed password
    db_user = User(
        email=user_data.email,
        name=user_data.name,
        hashed_password=get_password_hash(user_data.password)  # Add password hashing
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    # Create access token
    access_token = create_access_token(data={"sub": db_user.id, "email": db_user.email})

    return create_success_response(
        data={
            "user": UserResponse(
                id=db_user.id,
                email=db_user.email,
                name=db_user.name,
                created_at=db_user.created_at,
                updated_at=db_user.updated_at
            ),
            "token": access_token
        },
        message="User registered successfully"
    )


# Define a Pydantic model for login request
class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/login", response_model=dict)
async def login_user(
    login_data: LoginRequest,  # Accept request body as LoginRequest model
    session: Session = Depends(get_session)
):
    """Authenticate user and return access token"""
    email = login_data.email
    password = login_data.password

    # Find user by email
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()

    if not user or not user.hashed_password or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=create_error_response("AUTH_001", "Invalid credentials", 401)
        )

    # Create access token
    access_token = create_access_token(data={"sub": user.id, "email": user.email})

    return create_success_response(
        data={
            "user": UserResponse(
                id=user.id,
                email=user.email,
                name=user.name,
                created_at=user.created_at,
                updated_at=user.updated_at
            ),
            "token": access_token
        },
        message="Login successful"
    )

@router.post("/logout", response_model=dict)
async def logout_user():
    """Logout user (client-side only, no server state)"""
    return create_success_response(
        message="Logged out successfully"
    )