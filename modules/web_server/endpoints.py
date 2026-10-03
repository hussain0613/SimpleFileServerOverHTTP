import os

from fastapi import Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from settings import settings


templates = Jinja2Templates(directory="www")


async def file_server_ui(request: Request, dir_path: str | None = None) -> HTMLResponse:
    root_dir = settings.shared_directory # real path of root_directory
    
    if dir_path == None:
        dir_path = ""

    current_dir: str = os.path.join(root_dir, dir_path.lstrip("/\\")) # real path of current_directory

    # checking whether it is actually a dir or not
    if os.path.isfile(current_dir):
        return RedirectResponse(
            request.url_for("file_server.download", path=dir_path)
        )
    
    if not os.path.isdir(current_dir):
        return templates.TemplateResponse(request, name="error.html")
    
    return templates.TemplateResponse(request, name="index.html")


async def index(request: Request) -> RedirectResponse:
    return RedirectResponse(
        request.url_for("file_server_ui", dir_path = "")
    )


async def favicon() -> FileResponse:
    return FileResponse(
        path="www/statics/res/favicon.ico"
    )

