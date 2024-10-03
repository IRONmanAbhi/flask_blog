from flask import Blueprint, render_template, url_for, flash, redirect, request
from flaskblog import db, bcrypt
from flaskblog.users.forms import registrationForm, loginForm, accountUpdateForm, requestResetForm, resetPasswordForm
from flaskblog.models import User, Posts, UsedTokens
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog.users.utils import savePicture, send_reset_emails



users = Blueprint("users", __name__)

@users.route("/register", methods=['GET', 'POST'])
def register():
    if(current_user.is_authenticated):
        return redirect(url_for('main.home'))
    
    form = registrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        
        flash(f'Ypur account has been created! You can login to you account', 'success')
        return redirect(url_for("users.login"))
    return render_template('register.html', title='Register', form=form)

@users.route("/login", methods=['GET', 'POST'])
def login():
    if(current_user.is_authenticated):
        return redirect(url_for('main.home'))
    form = loginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if(user and bcrypt.check_password_hash(user.password, form.password.data)):
            login_user(user, remember=form.remember.data)
            flash(f"You have been logged in successfully", "success")
            nextPage = request.args.get('next')
            return redirect(nextPage) if nextPage else redirect(url_for("main.home"))
        else:
            flash("Login Unsuccessful. Please check Email and Password", "danger")
            return redirect(url_for("users.login"))
    return render_template("login.html", title = "users.Login", form = form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
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
        return redirect(url_for("users.account"))
    elif(request.method == 'GET'):
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename=f"profile_pics/{current_user.img_file}")
    return render_template("account.html", title="Account", image_file=image_file, form=form)


@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get("page", 1, int)
    user = User.query.filter_by(username=username).first_or_404()
    if(user != 404):
        posts = Posts.query.filter_by(author=user).order_by(Posts.date_posted.desc()).paginate(page=page, per_page=5)
        return render_template("user_posts.html", posts = posts, user=user)
    else:
        return "Error Page"


@users.route("/resetPassword", methods=['GET', 'POST'])
def reset_request():
    if(current_user.is_authenticated):
        return redirect(url_for("main.home"))
    form = requestResetForm()
    user = User.query.get(form.email.data)
    if(form.validate_on_submit()):
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_emails(user)
        flash("An email has been sent with instructions to reset password.", "info")
        return redirect(url_for("users.login"))
    return render_template("request_reset.html", title="Reset Password", form=form, user=user)

@users.route("/resetPassword/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if(current_user.is_authenticated):
        return redirect(url_for("main.home"))
    user_id = User.verify_reset_token(token)
    if(user_id is None):
        flash("That is an invalid or expired token", "warning")
        return redirect(url_for("users.reset_request"))
    form = resetPasswordForm()
    if(form.validate_on_submit()):
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user_id.password = hashed_password
        db.session.commit()
        flash("Successfully Password reset completed.", "success")
        newToken = UsedTokens(usedToken=token)
        db.session.add(newToken)
        db.session.commit()
        return redirect(url_for("users.login"))
    return render_template("reset_password.html", title="Reset Password", form=form)