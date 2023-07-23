from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate



app = Flask(__name__)
app.config["SECRET_KEY"] = "SECRET_KEYYYYYY"

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.db'
app.config['PROFILE_PICTURE_UPLOAD_FOLDER'] = 'static/profile_pictures'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'



from ecohabitat import views
