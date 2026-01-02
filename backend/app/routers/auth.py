"""Authentication router with signup, signin, and user endpoints."""

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.core.security import hash_password, verify_password, create_jwt_token, extract_user_id_from_token
from app.core.config import settings
from app.database import get_engine
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, AuthResponse

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


def get_db():
    """Get database session."""
    engine = get_engine()
    with Session(engine) as session:
        yield session


@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user with email and password."""

    # Check if user already exists
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Create new user with hashed password
    user = User(
        email=user_data.email,
        password_hash=hash_password(user_data.password)
    )

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Generate JWT token
    token = create_jwt_token(user_id=user.id, email=user.email)

    return AuthResponse(token=token, user=UserResponse.model_validate(user))


@router.post("/signin", response_model=AuthResponse)
async def signin(email: str, password: str, db: Session = Depends(get_db)):
    """Authenticate user and return JWT token."""

    # Find user by email
    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Generate JWT token
    token = create_jwt_token(user_id=user.id, email=user.email)

    return AuthResponse(token=token, user=UserResponse.model_validate(user))


@router.get("/me", response_model=UserResponse)
async def get_current_user(authorization: str = None, db: Session = Depends(get_db)):
    """Get current authenticated user's information."""

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    token = authorization.replace("Bearer ", "")
    user_id = extract_user_id_from_token(token)

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return UserResponse.model_validate(user)
