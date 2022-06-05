from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
	title = StringField('Başlık', validators=[DataRequired()])
	content = TextAreaField("İçerik", validators=[DataRequired()])
	submit = SubmitField("Paylaş")
	#so now lets create an instance of this form in our route and pass it in to our create post template