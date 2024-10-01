from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt
from flaskblog.form import registrationForm, loginForm, accountUpdateForm, postForm
from flaskblog.models import User, Posts
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
from PIL import Image

@app.route("/")
@app.route("/home")
def home():
    page = request.args.get("page", 1, int)
    posts = Posts.query.order_by(Posts.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template("home.html", posts = posts)


@app.route("/about")
def about():
    return render_template("about.html", title = "About Page")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if(current_user.is_authenticated):
        return redirect(url_for('home'))
    
    form = registrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        
        flash(f'Ypur account has been created! You can login to you account', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if(current_user.is_authenticated):
        return redirect(url_for('home'))
    form = loginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if(user and bcrypt.check_password_hash(user.password, form.password.data)):
            login_user(user, remember=form.remember.data)
            flash(f"You have been logged in successfully", "success")
            nextPage = request.args.get('next')
            return redirect(nextPage) if nextPage else redirect(url_for("home"))
        else:
            flash("Login Unsuccessful. Please check Email and Password", "danger")
            return redirect(url_for("login"))
    return render_template("login.html", title = "Login", form = form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def savePicture(form_picture, old_name):
    if( old_name != "default.jpg"):
        picPath = os.path.join(app.root_path, "static/profile_pics", old_name)
        if os.path.exists(picPath):
            os.remove(picPath)
            
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    new_name = random_hex + f_ext
    pic_path = os.path.join(app.root_path, "static/profile_pics", new_name)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(pic_path)
    return new_name

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form =  accountUpdateForm()
    if(form.validate_on_submit()):
        image_file = form.picture.data
        new_name= ""
        if(image_file):
            old_name = current_user.img_file
            new_name = savePicture(image_file, old_name)
            current_user.img_file = new_name
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account details have been successfully Updated", "success")
        return redirect(url_for("account"))
    elif(request.method == 'GET'):
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename=f"profile_pics/{current_user.img_file}")
    return render_template("account.html", title="Account", image_file=image_file, form=form)

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = postForm()
    if(form.validate_on_submit()):
        title = form.title.data
        content = form.content.data
        print(current_user.id)
        post = Posts(title=title, content=content, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash("Post has been created !", "success")
        return redirect(url_for("home"))
    return render_template("new_post.html", title="New Post", form=form)


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Posts.query.get_or_404(post_id)
    return render_template("post.html", title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Posts.query.get_or_404(post_id)
    if(current_user != post.author):
        abort(403)
    form = postForm()
    if(form.validate_on_submit()):
        post.title = form.title.data
        post.content = form.content.data
        post.edited = True
        db.session.commit()
        flash("Post has been Updated !", "success")
        return redirect(url_for("home"))
    elif(request.method == 'GET'):
        form.title.data = post.title
        form.content.data = post.content
    return render_template("update_post.html", title="Update Post", form=form)


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Posts.query.get_or_404(post_id)
    if(current_user != post.author):
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been Deleted", "success")
    return redirect(url_for("home"))


@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get("page", 1, int)
    user = User.query.filter_by(username=username).first_or_404()
    if(user != 404):
        posts = Posts.query.filter_by(author=user).order_by(Posts.date_posted.desc()).paginate(page=page, per_page=5)
        return render_template("user_posts.html", posts = posts, user=user)
    else:
        return "Error Page"