from app.db import get_connection


def create(workout_id: int, name: str, sets: int = 3, reps: int = 10,
           duration_seconds: int = 0, sort_order: int = 0) -> dict:
    """Добавить новое упражнение в БД и вернуть его в виде словаря."""
    with get_connection() as conn:
        cur = conn.execute(
            "INSERT INTO exercises (workout_id, name, sets, reps, duration_seconds, sort_order)"
            " VALUES (?, ?, ?, ?, ?, ?)",
            (workout_id, name, sets, reps, duration_seconds, sort_order),
        )
        conn.commit()
        return get_by_id(cur.lastrowid)


def get_by_workout(workout_id: int) -> list[dict]:
    """Вернуть все упражнения тренировки, отсортированные по sort_order."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM exercises WHERE workout_id = ? ORDER BY sort_order",
            (workout_id,),
        ).fetchall()
        return [dict(r) for r in rows]


def get_by_id(exercise_id: int) -> dict | None:
    """Вернуть упражнение по id в виде словаря, или None если не найдено."""
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM exercises WHERE id = ?", (exercise_id,)).fetchone()
        return dict(row) if row else None


def update(exercise_id: int, fields: dict) -> dict:
    """Обновить указанные поля упражнения и вернуть обновлённую запись."""
    if not fields:
        return get_by_id(exercise_id)
    set_clause = ", ".join(f"{k} = ?" for k in fields)
    values = list(fields.values()) + [exercise_id]
    with get_connection() as conn:
        conn.execute(f"UPDATE exercises SET {set_clause} WHERE id = ?", values)
        conn.commit()
    return get_by_id(exercise_id)


def delete(exercise_id: int) -> None:
    """Удалить упражнение по id."""
    with get_connection() as conn:
        conn.execute("DELETE FROM exercises WHERE id = ?", (exercise_id,))
        conn.commit()
