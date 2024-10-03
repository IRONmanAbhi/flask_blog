from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flaskblog import db
from flaskblog.posts.forms import postForm
from flaskblog.models import Posts
from flask_login import current_user, login_required


posts = Blueprint("posts", __name__)

@posts.route("/post/new", methods=['GET', 'POST'])
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
        return redirect(url_for("main.home"))
    return render_template("new_post.html", title="New Post", form=form)


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Posts.query.get_or_404(post_id)
    return render_template("post.html", title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
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
        return redirect(url_for("main.home"))
    elif(request.method == 'GET'):
        form.title.data = post.title
        form.content.data = post.content
    return render_template("update_post.html", title="Update Post", form=form)


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Posts.query.get_or_404(post_id)
    if(current_user != post.author):
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been Deleted", "success")
    return redirect(url_for("main.home"))