from fastapi import HTTPException

from app.models import workouts as workout_model
from app.models import exercises as exercise_model


def _require_trainer(user: dict) -> None:
    if user["role"] != "trainer":
        raise HTTPException(status_code=403, detail="Доступно только тренерам")


def _require_owner(workout: dict, user: dict) -> None:
    if workout["trainer_id"] != user["id"]:
        raise HTTPException(status_code=403, detail="Нет прав на редактирование")


def _with_exercises(workout: dict) -> dict:
    workout["exercises"] = exercise_model.get_by_workout(workout["id"])
    return workout


def list_all() -> list[dict]:
    """Вернуть все тренировки вместе с упражнениями."""
    return [_with_exercises(w) for w in workout_model.get_all()]


def get(workout_id: int) -> dict:
    """Вернуть тренировку с упражнениями; вызвать 404 если не найдена."""
    workout = workout_model.get_by_id(workout_id)
    if not workout:
        raise HTTPException(status_code=404, detail="Тренировка не найдена")
    return _with_exercises(workout)


def create(title: str, description: str, user: dict) -> dict:
    """Создать тренировку для тренера и вернуть её вместе с упражнениями."""
    _require_trainer(user)
    return _with_exercises(workout_model.create(title, description, user["id"]))


def update(workout_id: int, fields: dict, user: dict) -> dict:
    """Обновить допустимые поля тренировки; проверяет право владения."""
    _require_trainer(user)
    workout = workout_model.get_by_id(workout_id)
    if not workout:
        raise HTTPException(status_code=404, detail="Тренировка не найдена")
    _require_owner(workout, user)
    allowed = {k: v for k, v in fields.items() if k in ("title", "description") and v is not None}
    return _with_exercises(workout_model.update(workout_id, allowed))


def remove(workout_id: int, user: dict) -> None:
    """Удалить тренировку; проверяет роль тренера и право владения."""
    _require_trainer(user)
    workout = workout_model.get_by_id(workout_id)
    if not workout:
        raise HTTPException(status_code=404, detail="Тренировка не найдена")
    _require_owner(workout, user)
    workout_model.delete(workout_id)
