from app.db import get_connection


def create(title: str, description: str, trainer_id: int) -> dict:
    """Добавить новую тренировку в БД и вернуть её в виде словаря."""
    with get_connection() as conn:
        cur = conn.execute(
            "INSERT INTO workouts (title, description, trainer_id) VALUES (?, ?, ?)",
            (title, description, trainer_id),
        )
        conn.commit()
        return get_by_id(cur.lastrowid)


def get_all() -> list[dict]:
    """Вернуть все тренировки, отсортированные по дате создания (новые первые)."""
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM workouts ORDER BY created_at DESC").fetchall()
        return [dict(r) for r in rows]


def get_by_id(workout_id: int) -> dict | None:
    """Вернуть тренировку по id в виде словаря, или None если не найдена."""
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM workouts WHERE id = ?", (workout_id,)).fetchone()
        return dict(row) if row else None


def update(workout_id: int, fields: dict) -> dict:
    """Обновить указанные поля тренировки и вернуть обновлённую запись."""
    if not fields:
        return get_by_id(workout_id)
    set_clause = ", ".join(f"{k} = ?" for k in fields)
    values = list(fields.values()) + [workout_id]
    with get_connection() as conn:
        conn.execute(f"UPDATE workouts SET {set_clause} WHERE id = ?", values)
        conn.commit()
    return get_by_id(workout_id)


def delete(workout_id: int) -> None:
    """Удалить тренировку и все её упражнения по id."""
    with get_connection() as conn:
        conn.execute("DELETE FROM workouts WHERE id = ?", (workout_id,))
        conn.commit()
