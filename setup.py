import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask import Flask


app = Flask(__name__, template_folder='templates')
#########################################################################################
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secure-default-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', "postgresql://default:anh2IPVY0XDv@ep-billowing-violet-a4uz9d3l-pooler.us-east-1.aws.neon.tech:5432/verceldb?sslmode=require")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#########################################################################################
db = SQLAlchemy(app)
Migrate(app,db)
#########################################################################################
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "user_authentication_bp.user_login"
#########################################################################################
 