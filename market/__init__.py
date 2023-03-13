from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(user='root', password='', server='localhost', database='test')#'mysql:///foyya11:yadisetiadi1@localhost/market.db'
app.config['SECRET_KEY'] = 'd07be0c8f3ed94ba90a2a9fe'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"
from market import routes