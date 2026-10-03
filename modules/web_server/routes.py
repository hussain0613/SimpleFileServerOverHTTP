from fastapi import APIRouter

import modules.web_server.endpoints as endpoints

from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles


router = APIRouter(prefix="", tags=["web-server"])

router.mount(
    "/statics",
    StaticFiles(directory="www/statics"), 
    name="statics"
)


router.add_api_route(
    path="/favicon.ico",
    endpoint=endpoints.favicon,
    methods=["GET"],
    response_class=FileResponse
)


router.add_api_route(
    path="/fs/{dir_path:path}",
    endpoint=endpoints.file_server_ui,
    methods=["GET"],
    name="file_server_ui",
    response_class=HTMLResponse
)


router.add_api_route(
    path="/",
    endpoint=endpoints.index,
    name="index",
    response_class=RedirectResponse
)

