from flask import Flask, render_template, url_for, flash, redirect
from form import registrationForm, loginForm

app = Flask(__name__)

app.config["SECRET_KEY"] = "8389a9cec477d2ab55aa06fc0fbcc96c"
# this should be kept as an environment variable

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
def home():
    return render_template("home.html", posts = posts)


@app.route("/about")
def about():
    return render_template("about.html", title = "About Page")

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = registrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = loginForm()
    if form.validate_on_submit():
        if(form.email.data == "test@test.com"):
            flash(f"You have been logged in", "success")
            return redirect(url_for("home"))
        else:
            flash("Log in unsuccessful. Please check your credentials", "danger")
    return render_template("login.html", title = "Login", form = form)
    

if __name__ == "__main__":
    app.run(debug=True)