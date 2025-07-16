# Сервис для регистрации на научные конференции
## Установка
- перед установкой добавьте в переменные окружения
  
POSTGRES_USER=

POSTGRES_PASSWORD=

POSTGRES_DB=

POSTGRES_HOST=

POSTGRES_PORT=

REDIS_HOST=

REDIS_PORT=

- установка зависимостей
```python
python3 -m venv venv
source venv/bin/activate
pip install -e .
poetry install
docker-compose up
```
- установка миграций (запускать из src/yo/application/postgres)
```python
alembic upgrade head
```
- запуск
запустить файл src/yo/presentation/main.py из директории src/yo/

## Стэк: FastAPI, Redis, Postgres, SQLAlchemy + third party libs

