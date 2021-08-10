from utils import read_settings
settings = read_settings()

import os
from flask import Flask, Blueprint, render_template, send_from_directory

bp = Blueprint(__name__, "main")

@bp.route("/favicon.ico")
def favicon():
    return send_from_directory(directory = os.path.join(bp.root_path, "www", "statics", "res"), path="favicon.ico")

@bp.route("/")
def index():
    return render_template("index.html")





def create_app():
    app = Flask(__name__, template_folder="www", static_url_path="/statics", static_folder="www/statics")

    
    app.register_blueprint(bp)

    return app



if __name__ == "__main__":
    create_app().run(host=settings["host"], port=settings["port"], debug=True)
