import json, os, datetime

def get_default_settings()->dict:
    return {
    "shared_directory": os.path.expanduser("~"),
    "upload_permission": True,
    "modify_permission": True,
    "host": "0.0.0.0",
    "port": 9921,
    "debug": True,
    "max_upload_content_length_MB": None
}


def write_settings(settings: dict) -> None:
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


def get_human_readable_size(size_in_bytes) -> str:
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

def run_fast_scandir(query: str, contents: dict, cdir: str, rdir: str) -> list[str]:    # dir: str, ext: list
    """
    gives contents in the passed contents,
    a modified version of the code given in this answer: https://stackoverflow.com/a/59803793
    """
    subfolders = []
    try:
        for f in os.scandir(cdir):
            if f.is_dir():
                subfolders.append(f.path)
            
            if query.lower() in f.name.lower():
                dets = {}
                dets["name"] = f.name
                stats = os.stat(f.path)
                dets["date"] = datetime.datetime.fromtimestamp(stats.st_ctime)
                rel_path = f.path[len(rdir.rstrip("/\\")):] # relative to root_directory
                dets["directory"] = os.path.dirname(rel_path)
                contents[rel_path] = dets
                if f.is_dir():
                    subfolders.append(f.path)
                    dets["is_directory"] = True
                    dets["size"] = "-"
                if f.is_file():
                    dets["is_directory"] = False
                    dets["size"] = get_human_readable_size(stats.st_size)
                    #files.append((f.name, f.path))
    except PermissionError as err:
        pass
    
    for dir in list(subfolders):
        sf = run_fast_scandir(query, contents, dir, rdir)
        subfolders.extend(sf)
        #files.extend(f)
    return subfolders


