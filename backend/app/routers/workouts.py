from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional

from app.services import workout_service, user_service
from app.services.auth import get_current_user_id

router = APIRouter(prefix="/api/workouts", tags=["workouts"])


class WorkoutBody(BaseModel):
    title: str
    description: str = ""


class WorkoutPatch(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


@router.get("")
def list_workouts():
    """Вернуть все тренировки вместе с упражнениями."""
    return workout_service.list_all()


@router.get("/{workout_id}")
def get_workout(workout_id: int):
    """Вернуть одну тренировку вместе с её упражнениями."""
    return workout_service.get(workout_id)


@router.post("", status_code=201)
def create_workout(body: WorkoutBody, user_id: int = Depends(get_current_user_id)):
    """Создать новую тренировку (только для тренеров)."""
    user = user_service.get(user_id)
    return workout_service.create(body.title, body.description, user)


@router.patch("/{workout_id}")
def update_workout(workout_id: int, body: WorkoutPatch, user_id: int = Depends(get_current_user_id)):
    """Обновить название или описание тренировки (только для владельца)."""
    user = user_service.get(user_id)
    return workout_service.update(workout_id, body.model_dump(), user)


@router.delete("/{workout_id}", status_code=204)
def delete_workout(workout_id: int, user_id: int = Depends(get_current_user_id)):
    """Удалить тренировку и все её упражнения (только для владельца)."""
    user = user_service.get(user_id)
    workout_service.remove(workout_id, user)
