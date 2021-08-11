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
    with open("server_settings.json", "w") as file:
        file.write(json.dumps(settings))


def read_settings() -> dict:
    data: str
    try:
        with open("server_settings.json", "r") as file:
            data = file.read()
        return json.loads(data)

    except (FileNotFoundError) as err:
        write_settings(get_default_settings())


def get_human_readable_size(size_in_bytes):
    n = size_in_bytes
    suffix = "B"

    if n/10.0**9.0 > 1.0:
        n /= 10.0**9.0
        suffix = "GB"
    
    elif n/10.0**6.0 > 1.0:
        n /= 10.0**6.0
        suffix = "MB"
    elif n/10.0**3.0 > 1.0:
        n /= 10.0**3.0
        suffix = "KB"
    
    return f"{round(n, 2)}{suffix}"

