from fastapi import APIRouter

import modules.file_server_api.endpoints as endpoints

router = APIRouter(prefix="", tags=["file-server-api"])


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
