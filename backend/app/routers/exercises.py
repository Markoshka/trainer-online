from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional

from app.services import exercise_service, user_service
from app.services.auth import get_current_user_id

router = APIRouter(prefix="/api/exercises", tags=["exercises"])


class ExerciseBody(BaseModel):
    name: str
    sets: int = 3
    reps: int = 10
    duration_seconds: int = 0
    sort_order: int = 0


class ExercisePatch(BaseModel):
    name: Optional[str] = None
    sets: Optional[int] = None
    reps: Optional[int] = None
    duration_seconds: Optional[int] = None
    sort_order: Optional[int] = None


@router.post("/{workout_id}", status_code=201)
def add_exercise(workout_id: int, body: ExerciseBody, user_id: int = Depends(get_current_user_id)):
    """Добавить упражнение в тренировку (только для тренера-владельца)."""
    user = user_service.get(user_id)
    return exercise_service.add(workout_id, body.name, body.sets, body.reps,
                                body.duration_seconds, body.sort_order, user)


@router.patch("/{exercise_id}")
def update_exercise(exercise_id: int, body: ExercisePatch, user_id: int = Depends(get_current_user_id)):
    """Обновить упражнение (только для тренера-владельца)."""
    user = user_service.get(user_id)
    return exercise_service.update(exercise_id, body.model_dump(), user)


@router.delete("/{exercise_id}", status_code=204)
def delete_exercise(exercise_id: int, user_id: int = Depends(get_current_user_id)):
    """Удалить упражнение (только для тренера-владельца)."""
    user = user_service.get(user_id)
    exercise_service.remove(exercise_id, user)
