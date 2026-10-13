from fastapi import APIRouter

import modules.file_server_api.endpoints as endpoints

router = APIRouter(prefix="/api", tags=["file-server-api"])


router.add_api_route(
    path="/settings/",
    endpoint=endpoints.get_settings,
    methods=["GET"],
    name="get_settings"
)

router.add_api_route(
    path="/contents/",
    endpoint=endpoints.get_contents,
    methods=["GET"],
    name="get_contents"
)

router.add_api_route(
    "/download/",
    endpoint=endpoints.download_file,
    methods=["GET"],
    name="download_file"
)
