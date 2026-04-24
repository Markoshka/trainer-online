from app.db import get_connection


def create(name: str, email: str, password_hash: str, role: str = "client") -> dict:
    with get_connection() as conn:
        cur = conn.execute(
            "INSERT INTO users (name, email, password_hash, role) VALUES (?, ?, ?, ?)",
            (name, email, password_hash, role),
        )
        conn.commit()
        return get_by_id(cur.lastrowid)


def get_by_name(name: str) -> dict | None:
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM users WHERE name = ?", (name,)).fetchone()
        return dict(row) if row else None


def get_by_email(email: str) -> dict | None:
    """Вернуть пользователя по email в виде словаря, или None если не найден."""
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        return dict(row) if row else None


def get_by_id(user_id: int) -> dict | None:
    """Вернуть пользователя по id в виде словаря, или None если не найден."""
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        return dict(row) if row else None
