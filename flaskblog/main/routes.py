from flask import Blueprint, render_template, request
from flaskblog.models import Posts


main = Blueprint("main", __name__)

@main.route("/")
@main.route("/home")
def home():
    page = request.args.get("page", 1, int)
    posts = Posts.query.order_by(Posts.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template("home.html", posts = posts)


@main.route("/about")
def about():
    return render_template("about.html", title = "About Page")