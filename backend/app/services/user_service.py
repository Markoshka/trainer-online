from fastapi import HTTPException

from app.models import users as user_model
from app.services.auth import hash_password, verify_password, create_token


def register(name: str, email: str, password: str, role: str = "client") -> dict:
    if user_model.get_by_email(email):
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")
    return user_model.create(name, email, hash_password(password), role)


def login(username: str, password: str) -> str:
    user = user_model.get_by_name(username)
    if not user or not verify_password(password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Неверное имя пользователя или пароль")
    return create_token(user["id"])


def get(user_id: int) -> dict:
    """Вернуть пользователя по id; вызвать 404 если не найден."""
    user = user_model.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user
