from flask import Blueprint, render_template, current_app
import os

errors = Blueprint("errors", __name__)

@errors.app_errorhandler(404)
def error_404(error):
    picPath = os.path.join(current_app.root_path, "static/987654567.jpeg")
    return render_template("errors/404.html", picPath=picPath), 404

@errors.app_errorhandler(403)
def error_403(error):
    return render_template("errors/403.html"), 403

@errors.app_errorhandler(500)
def error_500(error):
    return render_template("errors/500.html"), 500

