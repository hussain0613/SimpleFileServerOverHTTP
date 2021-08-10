import json

def get_default_settings()->dict:
    return {
    "shared_directory": "D:/",
    "upload_permission": True,
    "modify_permission": True,
    "host": "0.0.0.0",
    "port": 9921
}


def write_settings(settings: dict):
    with open("settings.json", "w") as file:
        file.write(json.dumps(settings))


def read_settings() -> dict:
    data: str
    try:
        with open("settings.json", "r") as file:
            data = file.read()
        return json.loads(data)

    except (FileNotFoundError) as err:
        write_settings(get_default_settings())
