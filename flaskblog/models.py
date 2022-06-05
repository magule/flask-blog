from flaskblog import db, login_manager
from datetime import datetime #ikinci datetime issss class
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
#burdaki dbModel lar database in structini represent edeceh. bunlari databesi i create etmek icin kullanacagiz. terminal ile.
#usermixin login sessionlari icin fln. check again anyway.
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True) #primary_key=true a uniqie id for user.....
	username = db.Column(db.String(20), unique=True, nullable=False) #string 20 olmasinin nedeni max username.. uniqie olmasi da abvious zati... nulable=false da null olmasini engeller usernamin
	email = db.Column(db.String(120), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
	password = db.Column(db.String(60), nullable=False)
	posts = db.relationship('Post', backref='author', lazy=True) #check again


	def get_reset_token(self, expires_sec=1800): #forgot email etc. 10... check these again
		s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
		return s.dumps({"user_id": self.id}).decode('utf-8') #returning token whic is created by dumps method and it also contains a payload of the current userID

	@staticmethod
	def verify_reset_token(token): #check these again
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			user_id = s.loads(token['user_id'])
		except:
			return None
		return User.query.get(user_id)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False) 
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) #check again

	def __repr__(self):
		return f"User('{self.title}', '{self.date_posted}')"
