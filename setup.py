import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask import Flask
from flask import render_template


app = Flask(__name__, template_folder='templates')
#########################################################################################
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')
#########################################################################################
app.config['SECRET_KEY'] = 'mysecret'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#########################################################################################
db = SQLAlchemy(app)
Migrate(app,db)
#########################################################################################
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "user_login_bp.user_login"
#########################################################################################
from user_site.user_home.views import user_home_bp
from user_site.user_login.views import user_login_bp
from error_handlers import error_pages_bp

app.register_blueprint(user_home_bp)
app.register_blueprint(user_login_bp)
app.register_blueprint(error_pages_bp)