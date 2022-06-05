from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(title=form.title.data, content=form.content.data, author=current_user) #databese e eklemek icin. right? yup. right under this.
		db.session.add(post)
		db.session.commit()
		flash("Gonderi olusturuldu.", "success")
		return redirect(url_for("main.home"))
	return render_template("create_post.html", title="Yeni Gönderi", form=form, legend="Yeni Gönderi") #post=post diyerek we're passing that above in to our template



@posts.route("/post/<int:post_id>") #a page for a spesfic post.
def post(post_id):
	post = Post.query.get_or_404(post_id) #fetching the post if its exist. for a spesific post obviously.
	return render_template("post.html", title=post.title, post=post) #post=post passing in post to template?



@posts.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
	post = Post.query.get_or_404(post_id) #fetching the post if its exist.
	if post.author != current_user: #sadece kendi postunu edit yapabilir demek.
		abort(403) 
	form = PostForm()
	if form.validate_on_submit():
		post.title = form.title.data
		post.content = form.content.data
		db.session.commit() #already in the databese sooo we dont need db session add
		flash("gönderin guncellendi", "success")
		return redirect(url_for('posts.post', post_id=post.id)) #guncelledikten sonra o post a redirect et
	elif request.method == "GET": #benzerini hatta aynisini yapmistik.
		form.title.data = post.title
		form.content.data = post.content #bu ve yukardaki edit alaninda eski postun verilerinin gorunmesini saglar
	return render_template("create_post.html", title="Update Post",
	 form=form, legend="Gönderiyi Güncelle")


@posts.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
	post = Post.query.get_or_404(post_id) #fetching the post if its exist.
	if post.author != current_user: #sadece kendi postunu delete yapabilir demek.
		abort(403)
	db.session.delete(post)
	db.session.commit()
	flash("Gönderiniz silindi.", "success")
	return redirect(url_for('main.home'))
