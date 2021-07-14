## inputs ##
SHARED_DIRECTORY = "D:/"
HOST = "0.0.0.0"
PORT = 9999


import glob, os
from flask import Flask, render_template, redirect, send_file, request
from flask.helpers import url_for
import json


app = Flask(__name__)


SHARED_DIRECTORY = os.path.realpath(os.path.join(*os.path.split(SHARED_DIRECTORY))) ## processing

def check_existance_permission(path):
    if (SHARED_DIRECTORY != os.path.commonprefix([path, SHARED_DIRECTORY]) or not os.path.exists(path) or not os.access(path, os.R_OK)):
        return render_template("403.html")
    return 0

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


@app.route("/")
@app.route("/<path:directory>")
def index(directory=SHARED_DIRECTORY):

    check = check_existance_permission(directory)
    if(check != 0): return check

    directory = os.path.join(*os.path.split(directory))
    contents = os.listdir(directory)
    
    d = {}
    parent_directory = None
    if(directory != SHARED_DIRECTORY):
        parent_directory = os.path.dirname(directory)
        d[parent_directory] = ("<- parent_directory", "")

    for content in contents:
        # names.append(os.path.split(content)[-1])
        fullpath = os.path.join(directory, content)
        size = os.stat(fullpath).st_size
        d[fullpath] = (os.path.basename(content), get_human_readable_size(size))
    
    
    # print(f"************************************ current_directory = {directory}, contents: {contents}")
    # for k in d:
    #     print(f"******************************** {k}: {d[k]}")

    return render_template("index.html", d=d, os = os, directory = directory)

@app.route("/get_file/<path:file_name>")
def get_file(file_name):
    check = check_existance_permission(file_name)
    if(check != 0): return check

    if os.path.isdir(file_name):
        return redirect(url_for("index", directory = file_name))

    try:
        return send_file(file_name)
    except PermissionError as err:
        return render_template("403.html")


@app.route("/upload/<path:directory>", methods=["POST"])
def upload(directory):
    check = check_existance_permission(directory)
    if(check != 0): return check
    
    try:
        d = {}
        d["file_ids"] = []
        for file in request.files.getlist("files"):
            # file = request.files.get(f)
            fn = file.filename
            file.save(os.path.join(directory, fn))
            d["file_ids"].append(fn)
        
        d["status"] = "success"
        d["details"] = "file(s) saved"
        
        return json.dumps(d)
    except PermissionError:
        d["status"] = "failed"
        d["details"] = "no permission to upload in this directory"


@app.route("/search_result/")
def search():
    query = request.args.get("query")
    
    directory = SHARED_DIRECTORY
    contents = glob.glob(directory+f"**/{query}*")
    
    d = {}

    for content in contents:
        # names.append(os.path.split(content)[-1])
        fullpath = os.path.join(directory, content)
        size = os.stat(fullpath).st_size
        d[fullpath] = (os.path.basename(content), get_human_readable_size(size))
    
    
    # print(f"************************************ current_directory = {directory}, contents: {contents}")
    # for k in d:
    #     print(f"******************************** {k}: {d[k]}")

    return render_template("search.html", d=d, os = os, query = query)



if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=True)


