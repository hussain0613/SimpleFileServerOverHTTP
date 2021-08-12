from utils import read_settings, get_human_readable_size, run_fast_scandir
settings = read_settings()

import os, datetime
from flask import Flask, Blueprint, render_template, send_from_directory, request, redirect, url_for

bp = Blueprint("main", "main_bp")

@bp.route("/favicon.ico")
def favicon():
    return send_from_directory(directory = os.path.join(bp.root_path, "www", "statics", "res"), path="favicon.ico")

@bp.route("/get_contents/")
def get_contents():
    rdir = settings.get("shared_directory") # real path of root_directory
    dir_path: str = request.args.get("dir_path") # relative path, relative to settings["shared_directory"]
    if dir_path == None:
        dir_path = ""
    
    cdir: str = os.path.join(rdir, dir_path.lstrip("/\\")) # real path of current_directory
    
    # checking whether it is actually a dir or not
    if not os.path.isdir(cdir):
        return {"status": "failed", "details": "Not a directory!"}

    

    data = {"current_directory": dir_path}
    
    if(dir_path == "/" or dir_path == "\\" or dir_path == None or rdir == cdir): 
        data["parent_directory"] = None
    else:
        data["parent_directory"] = os.path.dirname(dir_path.rstrip("/\\")) 
    
    contents = {}
    try:
        fns = os.listdir(cdir) #folder or file names
        for fn in fns:
            details = {"name": fn}
            real_path: str = os.path.join(cdir, fn.lstrip("/\\"))
            stats = os.stat(real_path)
            
            isdir: bool = os.path.isdir(real_path)
            details["is_directory"] = isdir

            if isdir: details["size"] = "-"
            else: details["size"] = get_human_readable_size(stats.st_size)

            details["date"] = datetime.datetime.fromtimestamp(stats.st_ctime)     

            contents[os.path.join(dir_path, fn.lstrip("/\\"))] = details # key is the relative path
        data["contents"] = contents
        resp = {"status": "success", "details": "Fetched all contents of the given directory."}
        resp["data"] = data
        return resp
    except PermissionError as err:
        return {"status": "failed", "details": "Permission Denied!"}


@bp.route("/download/")
def download():
    rdir = settings.get("shared_directory") # real path of root_directory
    relative_path = request.args.get("path") # relative path
    
    if(relative_path == None): 
        return {"status": "failed", "details": "no file given"}

    path = os.path.join(rdir, relative_path.lstrip("/\\")) # real path

    if not os.path.exists(path):
        return {"status": "failed", "details": "Does not exist!"}
    
    if os.path.isdir(path):
        return {"status": "success", "details": "Actually not successfull. Downloading folders' not available yet."}
    
    try:
        return send_from_directory(directory=os.path.dirname(path), path=os.path.basename(path))
    except PermissionError as err:
        return {"status": "failed", "details": "Permission denied!"}


@bp.route("/get_settings/")
def get_settings():
    resp = {"status": "success", "details": "Fetched server settings."}
    global settings
    settings = read_settings()
    resp["settings"] = settings
    return resp


@bp.route("/upload_files/", methods=["POST"])
def upload_files():

    if settings.get("upload_permission") == False:
        return {"status": "failed", "details": "Upload permission not granted"}

    rdir = settings.get("shared_directory") # real path of root_directory
    relative_path = request.args.get("dir_path") # relative path
    
    if(relative_path == None): 
        return {"status": "failed", "details": "no directory given"}
    
    dir_path = os.path.join(rdir, relative_path.lstrip("/\\")) # real path

    if not os.path.exists(dir_path):
        return {"status": "failed", "details": "Does not exist!"}
    
    if not os.path.isdir(dir_path):
        return {"status": "failed", "details": "Not in a directory"}
    
    file_count: int = 0
    total_size: float = 0.0
    try:
        for file in request.files.getlist("files"):
            fn = file.filename
            
            f_path = os.path.join(dir_path, fn.lstrip("/\\")) # real path
            
            i = 2
            temp = f_path[:]
            while os.path.exists(temp):
                temp = f"_{i}.".join(f_path.rsplit(".", maxsplit=2))
                i += 1
            f_path = temp
            
            file.save(f_path)
            file_count += 1
            total_size += os.path.getsize(f_path)
            file.close()
            
        return {"status": "success", "details": f"Files saved successfully. Total {get_human_readable_size(total_size)} - {file_count} files"}
    except PermissionError as err:
        return {"status": "failed", "details": "Writing permission denied!"}
    

@bp.route("/create_directory/", methods=["POST"])
def create_directory():

    if settings.get("upload_permission") == False:
        return {"status": "failed", "details": "Upload permission not granted"}

    rdir = settings.get("shared_directory") # real path of root_directory
    relative_path = request.args.get("dir_path") # relative path

    if(relative_path == None): 
        return {"status": "failed", "details": "no direcoty given"}

    new_dir_name = request.args.get("new_dir_name")

    if(new_dir_name == None): 
        return {"status": "failed", "details": "no new directory name given given"}

    dir_path = os.path.join(rdir, relative_path.lstrip("/\\")) # real path

    if not os.path.exists(dir_path):
        return {"status": "failed", "details": "Does not exist!"}
    
    if not os.path.isdir(dir_path):
        return {"status": "failed", "details": "Not in a directory"}
      
    try:
        i: int = 2
        full_path = os.path.join(dir_path, new_dir_name.lstrip("/\\"))
        temp = full_path[:]
        while os.path.exists(temp):
            temp = full_path + "_" + str(i)
            i += 1
        full_path = temp

        os.mkdir(full_path)

        return {"status": "success", "details": f"Folder '{os.path.basename(full_path)}' created successfully."}
    except PermissionError as err:
        return {"status": "failed", "details": "Writing permission denied!"}



@bp.route("/get_search_result/")
def get_search_result():
    query = request.args.get("query")
    if(query == None):
        return {"status": "faield", "details": "no query given"}

    rdir: str = settings.get("shared_directory") # real path of root_directory
    dir_path: str = rdir
    
    relative_path: str = request.args.get("dir_path") # relative path
    
    if(relative_path != None): 
        dir_path = os.path.join(rdir, relative_path.lstrip("/\\")) # real path

        if not os.path.exists(dir_path):
            return {"status": "failed", "details": "given directory does not exist!"}
    
        if not os.path.isdir(dir_path):
            return {"status": "failed", "details": "given directory is not a directory"}

    data = {"current_directory": f"search result for '{query}'"}
    
    data["parent_directory"] = None
    
    contents = {}
    try:
        run_fast_scandir(query, contents, dir_path, rdir.rstrip("/\\"))
        
        data["contents"] = contents
        resp = {"status": "success", "details": f"fetched search result for '{query}'. *note: the search result might not show all the files matching the query"}
        resp["data"] = data
        return resp
    except PermissionError as err:
        return {"status": "failed", "details": "Permission Denied!"}




@bp.route("/fs/<path:dir_path>/")
@bp.route("/fs/")
def index(dir_path: str = None):
    rdir = settings.get("shared_directory") # real path of root_directory
    if dir_path == None:
        dir_path = ""

    cdir: str = os.path.join(rdir, dir_path.lstrip("/\\")) # real path of current_directory

    # checking whether it is actually a dir or not
    if os.path.isfile(cdir):
        return redirect(url_for("main.download", path=[dir_path]))
    
    if not os.path.isdir(cdir):
        return render_template("error.html")
    
    return render_template("index.html")


@bp.route("/")
def redirect_to_index():
    return redirect(url_for("main.index", dir_path = ""))




def create_app():
    app = Flask(__name__, template_folder="www", static_url_path="/statics", static_folder="www/statics")
    if(settings.get("max_upload_content_length_MB")) != None: app.config["MAX_CONTENT_LENGTH"] = settings.get("max_upload_content_length_MB") * 1000 * 1000
    
    app.register_blueprint(bp)

    return app


