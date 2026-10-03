from datetime import datetime
from pydantic import BaseModel

from settings import ServerSettings


class BaseResponse(BaseModel):
    status: str
    details: str


class ContentsResponseContent(BaseModel):
    name: str
    is_directory: bool
    size: str
    date: datetime


class ContentResponseData(BaseModel):
    current_directory: str
    parent_directory: str | None = None
    contents: dict[str, ContentsResponseContent]


class ContentsResponse(BaseResponse):
    data: ContentResponseData | None = None
    

class SettingsResponse(BaseResponse):
    settings: ServerSettings
