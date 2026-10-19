from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

from app.repositories.user import UserRepository
from app.utils.jwt import create_access_token, decode_token
from app.models.user import User, UserRole

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)
user_repository = UserRepository()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    username: str
    full_name: str
    role: UserRole

class UserResponse(BaseModel):
    user_id: int
    username: str
    full_name: str
    role: UserRole

    class Config:
        from_attributes = True

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = user_repository.authenticate(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    token = create_access_token(user)
    return Token(
        access_token=token,
        user_id=user.user_id,
        username=user.username,
        full_name=user.full_name,
        role=user.role,
    )

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    return User(
        user_id=int(user_id),
        username=payload.get("username"),
        password_hash="",
        full_name="",
        role=UserRole(payload.get("role")),
    )


@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user