from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr

from app.services import user_service
from app.services.auth import get_current_user_id

router = APIRouter(prefix="/api/users", tags=["users"])


class RegisterBody(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = "client"


class LoginBody(BaseModel):
    username: str
    password: str


@router.post("/register", status_code=201)
def register(body: RegisterBody):
    """Зарегистрировать новый аккаунт пользователя."""
    user = user_service.register(body.name, body.email, body.password, body.role)
    return {k: user[k] for k in ("id", "name", "email", "role", "created_at")}


@router.post("/login")
def login(body: LoginBody):
    """Аутентифицировать пользователя и вернуть JWT-токен."""
    token = user_service.login(body.username, body.password)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me")
def me(user_id: int = Depends(get_current_user_id)):
    """Вернуть профиль текущего авторизованного пользователя."""
    user = user_service.get(user_id)
    return {k: user[k] for k in ("id", "name", "email", "role", "created_at")}
