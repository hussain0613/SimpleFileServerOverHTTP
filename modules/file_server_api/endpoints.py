import asyncio
import datetime
import os

from fastapi import UploadFile
from fastapi.responses import FileResponse

from settings import settings

import modules.file_server_api.schemas as schemas
import modules.file_server_api.controllers as controllers


async def get_settings() -> schemas.SettingsResponse:
    return schemas.SettingsResponse(
        status = "success",
        details = "Fetched server settings.",
        settings = settings
    )


async def get_contents(dir_path: str | None = None) -> schemas.ContentsResponse:
    # dir_path -> relative path, relative to settings["shared_directory"]
 
    root_dir = settings.shared_directory # real path of root_directory
    if dir_path == None:
        dir_path = ""
    
    current_dir: str = os.path.join(root_dir, dir_path.lstrip("/\\")) # real path of current_directory
    
    # checking whether it is actually a dir or not
    if not os.path.isdir(current_dir):
        return {"status": "failed", "details": "Not a directory!"}

    

    data = {"current_directory": dir_path}
    
    if(dir_path == "/" or dir_path == "\\" or dir_path == None or root_dir == current_dir): 
        data["parent_directory"] = None
    else:
        data["parent_directory"] = os.path.dirname(dir_path.rstrip("/\\")) 
    
    contents = {}
    try:
        fns = os.listdir(current_dir) #folder or file names
        for fn in fns:
            details = {"name": fn}
            real_path: str = os.path.join(current_dir, fn.lstrip("/\\"))
            try:
                stats = os.stat(real_path)
            except FileNotFoundError:
                # Can happend for broken symlinks!
                # stats = os.lstat(real_path) # will get the stas for the symlink instead of the actual file
                continue
            
            isdir: bool = os.path.isdir(real_path)
            details["is_directory"] = isdir

            if isdir: details["size"] = "-"
            else: details["size"] = controllers.get_human_readable_size(stats.st_size)

            details["date"] = datetime.datetime.fromtimestamp(stats.st_ctime)     

            contents[os.path.join(dir_path, fn.lstrip("/\\"))] = details # key is the relative path
        data["contents"] = contents
        resp = {"status": "success", "details": "Fetched all contents of the given directory."}
        resp["data"] = data
        return resp
    except PermissionError as err:
        return {"status": "failed", "details": "Permission Denied!"}



async def download_file(path: str) -> FileResponse:
    root_dir = settings.shared_directory # real path of root_directory
    
    relative_path = path
    if(relative_path == None): 
        return {"status": "failed", "details": "no file given"}

    real_path = os.path.join(root_dir, relative_path.lstrip("/\\")) # real path

    if not os.path.exists(real_path):
        return {"status": "failed", "details": "Does not exist!"}
    
    if os.path.isdir(real_path):
        return {"status": "success", "details": "Actually not successfull. Downloading folders' not available yet."}

    filename = os.path.basename(real_path)
    
    try:
        return FileResponse(
            path=real_path,
            filename=filename
        )
    except PermissionError as err:
        return {"status": "failed", "details": "Permission denied!"}


async def search(query: str, dir_path: str) -> schemas.ContentsResponse:
    if(query == None):
        return {"status": "faield", "details": "no query given"}

    root_dir: str = settings.shared_directory # real path of root_directory
    search_dir: str = root_dir
    
    if(dir_path != None): # dir path is the relative path of the search dir from root dir
        search_dir = os.path.join(root_dir, dir_path.lstrip("/\\")) # real path

        if not os.path.exists(search_dir):
            return {"status": "failed", "details": "given directory does not exist!"}
    
        if not os.path.isdir(search_dir):
            return {"status": "failed", "details": "given directory is not a directory"}

    data = {"current_directory": f"search result for '{query}'"}
    
    data["parent_directory"] = None
    
    contents = {}
    try:
        await asyncio.to_thread(controllers.run_fast_scandir, query, contents, search_dir, root_dir.rstrip("/\\"))
        # controllers.run_fast_scandir(query, contents, search_dir, root_dir.rstrip("/\\"))
        
        data["contents"] = contents
        resp = {"status": "success", "details": f"fetched search result for '{query}'. *note: the search result might not show all the files matching the query"}
        resp["data"] = data
        return resp
    except PermissionError as err:
        return {"status": "failed", "details": "Permission Denied!"}


async def upload_files(dir_path: str, files: list[UploadFile]) -> schemas.BaseResponse:
    if settings.upload_permission == False:
        return {"status": "failed", "details": "Upload permission not granted"}

    root_dir = settings.shared_directory # real path of root_directory
    
    if(dir_path == None): # `dir_path` is the relative path of the dir
        return {"status": "failed", "details": "no directory given"}
    
    abs_dir_path = os.path.join(root_dir, dir_path.lstrip("/\\")) # real/absolute path

    if not os.path.exists(abs_dir_path):
        return {"status": "failed", "details": "Does not exist!"}
    
    if not os.path.isdir(abs_dir_path):
        return {"status": "failed", "details": "Not in a directory"}
    
    file_count: int = 0
    total_size: float = 0.0
    try:
        for file in files:
            file_path = os.path.join(abs_dir_path, file.filename.lstrip("/\\")) # real path

            file_path = await asyncio.to_thread(controllers.save_file, file_path, file.file)

            file_count += 1
            total_size += os.path.getsize(file_path)
            await file.close()

        return {"status": "success", "details": f"Files saved successfully. Total {controllers.get_human_readable_size(total_size)} - {file_count} files"}
    except PermissionError as err:
        return {"status": "failed", "details": "Writing permission denied!"}


async def create_directory(new_dir_name: str, dir_path: str) -> schemas.BaseResponse:
    if settings.upload_permission == False:
        return {"status": "failed", "details": "Upload permission not granted"}

    root_dir = settings.shared_directory # real path of root_directory

    if(dir_path == None): 
        return {"status": "failed", "details": "no direcoty given"}


    if(new_dir_name == None): 
        return {"status": "failed", "details": "no new directory name given given"}

    real_dir_path = os.path.join(root_dir, dir_path.lstrip("/\\")) # real path

    if not os.path.exists(real_dir_path):
        return {"status": "failed", "details": "Does not exist!"}

    if not os.path.isdir(real_dir_path):
        return {"status": "failed", "details": "Not in a directory"}

    try:
        i: int = 2
        full_path = os.path.join(real_dir_path, new_dir_name.lstrip("/\\"))
        temp = full_path[:]
        while os.path.exists(temp):
            temp = full_path + "_" + str(i)
            i += 1
        full_path = temp

        os.mkdir(full_path)

        return {"status": "success", "details": f"Folder '{os.path.basename(full_path)}' created successfully."}
    except PermissionError as err:
        return {"status": "failed", "details": "Writing permission denied!"}
