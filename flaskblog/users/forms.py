from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskblog.models import User


class RegistrationForm(FlaskForm):
	name = StringField("")

	surname = StringField()

	username = StringField("Kullanıcı Adı", validators=[DataRequired(), Length(min=2, max=20)])

	email = StringField("Email", validators=[DataRequired(), Email()])

	password = PasswordField("Şifre", validators=[DataRequired(), Length(min=4, max=50)])

	confirm_password = PasswordField("Şifreyi onayla", validators=[DataRequired(), Length(min=4, max=50), EqualTo("password")])

	submit = SubmitField("Kayıt Ol")
 
	def validate_username(self, username): #database de bu kullunaci varmi onu kontrol ediy
		user= User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError("bu kullanici adi daha onceden alinmis.")

	def validate_email(self, email): #database de bu kullunaci varmi onu kontrol ediy
		user= User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError("bu email daha onceden kullanilmis.")




class LoginForm(FlaskForm):
	email = StringField("Email", validators=[DataRequired(), Email()])

	password = PasswordField("Şifre", validators=[DataRequired(), Length(min=4, max=50)])

	remember = BooleanField("Beni Hatırla")
	
	submit = SubmitField("Giriş Yap")




class UpdateAccountForm(FlaskForm):
	username = StringField("Kullanıcı Adı", validators=[DataRequired(), Length(min=2, max=20)])

	email = StringField("Email", validators=[DataRequired(), Email()])

	picture = FileField("Profil fotografini guncelle.", validators=[FileAllowed(['jpg', 'png'])])

	submit = SubmitField("Güncelle")
 
	def validate_username(self, username): #database de bu kullunaci varmi onu kontrol ediy
		if username.data != current_user.username:
			user= User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError("bu kullanici adi daha onceden alinmis.")

	def validate_email(self, email): #database de bu kullunaci varmi onu kontrol ediy
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError("bu email daha onceden kullanilmis.")
			#now lets import this form we've created into our route. and than from there we can pass into our account template



class RequestResetForm(FlaskForm):
	email = StringField("Email", validators=[DataRequired(), Email()])
	submit = SubmitField("Sifreyi sifirla.")

	def validate_email(self, email): #database de bu kullunaci varmi onu kontrol ediy
		user = User.query.filter_by(email=email.data).first()
		if user is None:
			raise ValidationError("bu email ile kayıt olunan hesap yok")




class ResetPasswordForm(FlaskForm):
	password = PasswordField("Şifre", validators=[DataRequired(), Length(min=4, max=50)])
	confirm_password = PasswordField("Şifreyi tekrar gir.", validators=[DataRequired(), Length(min=4, max=50), EqualTo("password")])
	submit = SubmitField("Şifreyi sıfırla.")



