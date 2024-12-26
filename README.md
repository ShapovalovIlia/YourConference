# Сервис для регистрации на научные конференции
## work in progress
## Установка
запускать main.py из директории yo
- перед добавьте в переменные окружения
  
POSTGRES_USER=

POSTGRES_PASSWORD=

POSTGRES_DB=

POSTGRES_HOST=

POSTGRES_PORT=

REDIS_HOST=

REDIS_PORT=

```python
python3 -m venv venv
source venv/bin/activate
pip install -e .
poetry install
docker-compose up
```
## Стэк: FastAPI, Redis, Postgres, SQLAlchemy и несколько third party либ
### Явно стоит переделать:
- разделения слоя бизнес логики и ее реализации
(тут все лежит в application, это задумывалось специально, чтобы посмотреть на неудобства, которые это приносит и оценить увелечение скорости разработки при таком подоходе)
- добавить кастомные статус коды и их описание

### Немножко мыслей:
- использование ORM ломает слои абстракции, но увеличивает скорость разработки
- у FastAPI неудобный DI, в следующий раз попробую Dishka
- хочу попробовать другую орм вместо SQLAlchemy (например peewee) и FastAPI Users
