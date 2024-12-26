import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from uvicorn import Config, Server

from yo.presentation.routers import (
    auth_router,
    conference_router,
    review_router,
    registration_router,
    start_router,
)

from yo.application import ApplicationError


def application_error_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    if isinstance(exc, ApplicationError):
        return JSONResponse(status_code=400, content={"message": exc.message})

    return JSONResponse(
        status_code=500, content={"message": "Internal Server Error"}
    )


async def main() -> None:
    app = FastAPI(title="YourConference")

    config = Config(app=app, host="127.0.0.1", port=8080)
    server = Server(config=config)

    app.add_exception_handler(ApplicationError, application_error_handler)

    app.include_router(auth_router)
    app.include_router(conference_router)
    app.include_router(review_router)
    app.include_router(registration_router)
    app.include_router(start_router)

    await server.serve()


asyncio.run(main())
