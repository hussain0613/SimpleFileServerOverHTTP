from fastapi import FastAPI

from modules.file_server_api.routes import router as file_server_api_router
from modules.web_server.routes import router as web_server_router

def register_routers(app: FastAPI) -> None:
    app.include_router(web_server_router)
    app.include_router(file_server_api_router)


