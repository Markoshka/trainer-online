# Trainer Online

Платформа для онлайн-тренировок.

## Структура

```
trainer-online/
├── backend/          # FastAPI приложение
│   ├── app/
│   │   ├── models/   # Модели БД
│   │   ├── routers/  # API маршруты
│   │   ├── schemas/  # Pydantic схемы
│   │   └── services/ # Бизнес-логика
│   └── requirements.txt
├── frontend/         # Веб приложение
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── api/
│   └── package.json
├── docker-compose.yml
├── .gitignore
└── README.md
```
