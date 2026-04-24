from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.db import get_connection
from app.routers import users, workouts, exercises

app = FastAPI(title="Trainer Online API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(workouts.router)
app.include_router(exercises.router)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
        headers={"Access-Control-Allow-Origin": "*"},
    )


@app.on_event("startup")
def create_tables() -> None:
    """Создать все таблицы базы данных, если они не существуют."""
    with get_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                name          TEXT    NOT NULL,
                email         TEXT    UNIQUE NOT NULL,
                password_hash TEXT    NOT NULL,
                role          TEXT    NOT NULL DEFAULT 'client',
                created_at    TEXT    DEFAULT (datetime('now'))
            );
            CREATE TABLE IF NOT EXISTS workouts (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                title       TEXT    NOT NULL,
                description TEXT    DEFAULT '',
                trainer_id  INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                created_at  TEXT    DEFAULT (datetime('now'))
            );
            CREATE TABLE IF NOT EXISTS exercises (
                id               INTEGER PRIMARY KEY AUTOINCREMENT,
                workout_id       INTEGER NOT NULL REFERENCES workouts(id) ON DELETE CASCADE,
                name             TEXT    NOT NULL,
                sets             INTEGER DEFAULT 3,
                reps             INTEGER DEFAULT 10,
                duration_seconds INTEGER DEFAULT 0,
                sort_order       INTEGER DEFAULT 0
            );
        """)
        conn.commit()


@app.get("/")
def root():
    """Проверка работоспособности API."""
    return {"status": "ok", "message": "Trainer Online API"}
