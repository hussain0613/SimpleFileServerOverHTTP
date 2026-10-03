from fastapi import FastAPI

from modules.web_server.routes import router as web_server_router

def register_routers(app: FastAPI) -> None:
    app.include_router(web_server_router)


