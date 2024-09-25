from flask import Flask, render_template

app = Flask(__name__)

posts = [
    {
        "author":"Author 1",
        "title":"blog post 1",
        "content":"First post content",
        "date_posted":"April 20, 2019"
    },
    {
        "author":"Author 2",
        "title":"blog post 2",
        "content":"second post content",
        "date_posted":"April 30, 2019"
    }
]


@app.route("/")
@app.route("/home")
def hello_world():
    return render_template("home.html", posts = posts)


@app.route("/about")
def about():
    return render_template("about.html", title = "About Page")

if __name__ == "__main__":
    app.run(debug=True)