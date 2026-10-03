from fastapi import FastAPI

from modules.register_routers import register_routers


def create_app():

    app = FastAPI(
        title="SimpleFileServerOverHTTP"
    )

    register_routers(app)

    return app
