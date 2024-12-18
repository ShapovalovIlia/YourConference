import asyncio
from fastapi import FastAPI
from uvicorn import Config, Server
from yo.presentation import user_router, admin_router


async def main() -> None:
    app = FastAPI()

    config = Config(app=app, host="127.0.0.1", port=8080, reload=True)
    server = Server(config=config)
    app.include_router(user_router)
    app.include_router(admin_router)

    await server.serve()


asyncio.run(main())
