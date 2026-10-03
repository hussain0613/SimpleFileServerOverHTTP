import json
import os

from pydantic import BaseModel

class ServerSettings(BaseModel):
    shared_directory: str = os.path.expanduser("~")
    upload_permission: bool = True
    modify_permission: bool = True
    host: str = "0.0.0.0"
    port: int = 9921
    debug: bool = False

    @classmethod
    def write_settings(cls, settings: "ServerSettings", file_path: str = "server_settings.json") -> None:
        with open(file_path, "w") as f:
            json.dump(settings.model_dump(), f, indent=4)

    @classmethod
    def load_from_json(cls, file_path: str = "server_settings.json") -> "ServerSettings":
        with open(file_path, "r") as f:
            settings_data = json.load(f)
        return cls(**settings_data)

    @classmethod
    def load(cls) -> "ServerSettings":
        try:
            return cls.load_from_json()
        except FileNotFoundError:
            cls.write_settings(cls())
            return cls.load()



settings = ServerSettings.load()
    