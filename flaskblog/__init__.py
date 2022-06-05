from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager() 
login_manager.login_view = 'users.login' #didnt really understand why we added this. check on this again.
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(Config)

	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)

	from flaskblog.users.routes import users #burdaki users blueprint class in instance i
	from flaskblog.posts.routes import posts
	from flaskblog.main.routes import main
	from flaskblog.errors.handlers import errors #burdaki import errors errors = Blueprint('errors', __name__) burdan geliyor. handlers.py da

	app.register_blueprint(errors)
	app.register_blueprint(users)
	app.register_blueprint(posts)
	app.register_blueprint(main)

	return app

