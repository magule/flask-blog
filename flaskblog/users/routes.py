from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from flaskblog.users.utils import save_picture, send_reset_email


users = Blueprint('users', __name__)


@users.route("/register", methods=["GET", "POST"]) #burda methodlari eklemezsek method not allowed error u verecek. tekrar bi bak buna
def register():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') #form.password.data girilen sifre ilk kismi tekrar check btw.hashed_password = bcrypt.generate_password_hash fln.
		user = User(username=form.username.data, email=form.email.data, password=hashed_password) #creating user. user=User()i grasp well.
		db.session.add(user)
		db.session.commit()
		flash('Hesabiniz olusturuldu. Giris yapabilirsiniz.', 'success') #success bootstrap seysi
		return redirect(url_for("users.login")) #home burda route daki function un adi
	return render_template("register.html", title="Kayıt Ol", form=form)


#login i iyice anla tekrar calis.
@users.route("/login", methods=["GET", "POST"])
def login():
	if current_user.is_authenticated: #making sure that theyre logged out
		return redirect(url_for('main.home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data): #so if the user exist and the password they entered is valid with whats in the databese... #user.password databeseden gelicek since databese query is right on top. email ile eslesiyosa(ustte aldik) password (databeseden gelen ve girilen) devam et diyor basicly.
			login_user(user, remember=form.remember.data) #icine yazilan user this user anlamina gelir yani uniqly o kullaniciya bakiyoz.
			next_page = request.args.get('next') #44-6 cokda onemli bisey degil olmasada olur gibi.
			return redirect(next_page) if next_page else redirect(url_for('main.home')) #if next_page meaans if its not nun. if its exist
		else:
			flash("Giris basarisiz. Emaili ve sifreni dogru girdiginden emin ol!", "danger")
	return render_template("login.html", title="Giriş Yap", form=form) #form= form bi usttteki ile passin posts=posts da da en ustte var


@users.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('main.home'))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit(): #updating account info
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file
		current_user.username = form.username.data #suanki username i girilenle degistir 
		current_user.email = form.email.data
		db.session.commit()
		flash("güncellendi!!!", "success")
		return redirect(url_for("users.account"))
	elif request.method == "GET": #gucelleme sayfasinda eski (current) emailin fln gozukmesini saglar instead of empty space
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
	return render_template("account.html", title="Hesap", image_file=image_file, form=form) #image file = imagie file understand it well... ayrica burdaki form=form  yukardaki form=updateaccountform() dan geliy


#showing all the posts of a spesific user
@users.route("/user/<string:username>")
def user_posts(username): 
    page = request.args.get('page', 1, type=int) #istenilen sayfayi almak...type page number oluy yani birisi int den baska birsey girerese error.1 = default first page
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
    	.order_by(Post.date_posted.desc())\
    	.paginate(page=page, per_page=5)  #database den tum postlari al... page=page ile secilen page i query e  pass ediyoruk
    return render_template('user_posts.html', posts=posts, user=user) #passing in post to that template by doing posts=posts. and passing in user to that template by doing user=user




@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Email gönderildi', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Sifreyi sifirla.', form=form)



@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token): #where u actually reset ur password with the token
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	user = User.verify_reset_token(token)
	if user is None:
		flash('geçersiz yada süresi dolmuş token', 'warning')
		return redirect(url_for('users.reset_request'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') #form.password.data girilen sifre ilk kismi tekrar check btw.hashed_password = bcrypt.generate_password_hash fln.
		user.password = hashed_password
		db.session.commit()
		flash('Sifreniz guncellendi. Giris yapabilirsiniz.', 'success') #success bootstrap seysi
		return redirect(url_for("users.login")) #home burda route daki function un adi
	return render_template('reset_token.html', title="Sifreyi Sifirla", form=form)















