import asyncio
from fastapi import FastAPI
from uvicorn import Config, Server

from yo.presentation.routers import (
    auth_router,
    conference_router,
    review_router,
    registration_router,
)


async def main() -> None:
    app = FastAPI(title="lab2")

    config = Config(app=app, host="127.0.0.1", port=8080, reload=True)
    server = Server(config=config)
    app.include_router(auth_router)
    app.include_router(conference_router)
    app.include_router(review_router)
    app.include_router(registration_router)

    await server.serve()


asyncio.run(main())
