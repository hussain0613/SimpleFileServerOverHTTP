from utils import read_settings, get_human_readable_size
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
        return {"status": "failed", "details": "not a directory"}

    

    data = {"current_directory": dir_path}
    
    if(dir_path == "/" or dir_path == "\\" or dir_path == None or rdir == cdir): 
        data["parent_directory"] = None
    else:
        data["parent_directory"] = os.path.dirname(dir_path.rstrip("/\\")) 
    
    contents = {}
    #try:
    fns = os.listdir(cdir) #folder or file names
    for fn in fns:
        details = {"name": fn}
        real_path: str = os.path.join(cdir, fn)
        stats = os.stat(real_path)
        
        isdir: bool = os.path.isdir(real_path)
        details["is_directory"] = isdir

        if isdir: details["size"] = "-"
        else: details["size"] = get_human_readable_size(stats.st_size)

        details["date"] = datetime.datetime.fromtimestamp(stats.st_ctime)     

        contents[os.path.join(dir_path, fn)] = details # key is the relative path
    data["contents"] = contents
    resp = {"status": "success", "details": "fetched all contents of the given directory"}
    resp["data"] = data
    return resp


@bp.route("/download/")
def download():
    rdir = settings.get("shared_directory") # real path of root_directory
    relative_path = request.args.get("path") # relative path
    path = os.path.join(rdir, relative_path) # real path

    if not os.path.exists(path):
        return {"status": "failed", "details": "does not exist"}
    
    if os.path.isdir(path):
        return {"status": "success", "details": "eita folder, so ashole successful na, pore kora hobe"}
    
    return send_from_directory(directory=os.path.dirname(path), path=os.path.basename(path))


@bp.route("/<path:dir_path>/")
@bp.route("/")
def index(dir_path: str = None):
    rdir = settings.get("shared_directory") # real path of root_directory
    if dir_path == "" or dir_path == None:
        dir_path = "/"

    cdir: str = os.path.join(rdir, dir_path) # real path of current_directory

    # checking whether it is actually a dir or not
    if os.path.isfile(cdir):
        return redirect(url_for("main.download", path=[dir_path]))
    
    if not os.path.isdir(cdir):
        return render_template("error.html")
    
    return render_template("index.html")





def create_app():
    app = Flask(__name__, template_folder="www", static_url_path="/statics", static_folder="www/statics")

    
    app.register_blueprint(bp)

    return app



if __name__ == "__main__":
    create_app().run(host=settings["host"], port=settings["port"], debug=True)
