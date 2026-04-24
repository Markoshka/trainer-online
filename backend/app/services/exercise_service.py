from fastapi import HTTPException

from app.models import exercises as exercise_model
from app.models import workouts as workout_model


def _require_workout_owner(workout_id: int, user: dict) -> None:
    workout = workout_model.get_by_id(workout_id)
    if not workout:
        raise HTTPException(status_code=404, detail="Тренировка не найдена")
    if workout["trainer_id"] != user["id"]:
        raise HTTPException(status_code=403, detail="Нет прав на редактирование тренировки")


def add(workout_id: int, name: str, sets: int, reps: int,
        duration_seconds: int, sort_order: int, user: dict) -> dict:
    """Добавить упражнение в тренировку; проверяет право владения тренера."""
    _require_workout_owner(workout_id, user)
    return exercise_model.create(workout_id, name, sets, reps, duration_seconds, sort_order)


def update(exercise_id: int, fields: dict, user: dict) -> dict:
    """Обновить поля упражнения; проверяет право владения тренера на тренировку."""
    exercise = exercise_model.get_by_id(exercise_id)
    if not exercise:
        raise HTTPException(status_code=404, detail="Упражнение не найдено")
    _require_workout_owner(exercise["workout_id"], user)
    allowed_keys = ("name", "sets", "reps", "duration_seconds", "sort_order")
    allowed = {k: v for k, v in fields.items() if k in allowed_keys and v is not None}
    return exercise_model.update(exercise_id, allowed)


def remove(exercise_id: int, user: dict) -> None:
    """Удалить упражнение; проверяет право владения тренера на тренировку."""
    exercise = exercise_model.get_by_id(exercise_id)
    if not exercise:
        raise HTTPException(status_code=404, detail="Упражнение не найдено")
    _require_workout_owner(exercise["workout_id"], user)
    exercise_model.delete(exercise_id)
