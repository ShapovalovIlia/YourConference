# Сервис для регистрации на научные конференции
## work in progress
## Установка
- перед добавьте в переменные окружения
POSTGRES_USER=postgres
POSTGRES_PASSWORD=1234
POSTGRES_DB=YourConference
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
REDIS_HOST=127.0.0.1
REDIS_PORT=6379

'''python
python3 -m venv venv
source venv/bin/activate
pip install -e .
poetry install
'''
## Стэк: FastAPI, Redis, Postgres, SQLAlchemy и несколько third party либ
### Явно стоит переделать:
- разделения слоя бизнес логики и ее реализации
(тут все лежит в application, это задумывалось специально, чтобы посмотреть на неудобства, которые это приносит и оценить увелечение скорости разработки при таком подоходе)
- добавить кастомные статус коды и их описание

### Немножко мыслей:
- использование ORM ломает слои абстракции, но увеличивает скорость разработки
- у FastAPI неудобный DI, в следующий раз попробую Dishka
- хочу попробовать другую орм вместо SQLAlchemy (например peewee) и FastAPI Users
