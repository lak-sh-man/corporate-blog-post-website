from setup import db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    # Attempt to load User first
    user = User.query.get(user_id)
    if user:
        return user
    
    # If User not found, attempt to load Admin
    admin = Admin.query.get(user_id)
    if admin:
        return admin

    # If neither is found, return None
    return None

class User(db.Model, UserMixin):

    __tablename__ = 'user_table'

    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    profile_image = db.Column(db.String(255), nullable=True, default='user_default_profile.jpg')
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(255))
    posts = db.relationship('UserBlogPost', backref='user_author', lazy=True)
    admin_id = db.Column(db.Integer,db.ForeignKey('admin_table.id'), nullable=False)

    @classmethod
    def get_next_id(cls):
        # this "db.session" is SQLAlchemy session that delas with db
        # user session is different, it looks like just "session['username'] = username"
        max_id = db.session.query(db.func.max(cls.id)).scalar()
        return max_id + 1 if max_id else 1

    def __init__(self, id, email, username, password, admin_id):
        self.id = id
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.admin_id = admin_id

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f"id : {self.id} | client name : {self.username}"



class UserBlogPost(db.Model):

    __tablename__ = 'userblogpost_table'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(140), nullable=False)
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_table.id'), nullable=False)

    def __init__(self, title, text, user_id):
        self.title = title
        self.text = text
        self.user_id =user_id


    def __repr__(self):
        return f"Post Id: {self.id} --- Date: {self.date} --- Title: {self.title}"
    


class Admin(db.Model, UserMixin):

    __tablename__ = 'admin_table'

    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    profile_image = db.Column(db.String(255), nullable=False, default='admin_default_profile.jpg')
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(255))
    posts = db.relationship('AdminBlogPost', backref='admin_author', lazy=True)
    clients = db.relationship('User',backref='admin_clients',lazy='dynamic')

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f"UserName: {self.username}"



class AdminBlogPost(db.Model):

    __tablename__ = 'adminblogpost_table'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(140), nullable=False)
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('admin_table.id'), nullable=False)

    def __init__(self, title, text, user_id):
        self.title = title
        self.text = text
        self.user_id =user_id


    def __repr__(self):
        return f"Post Id: {self.id} --- Date: {self.date} --- Title: {self.title}"