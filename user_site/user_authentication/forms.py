# Form Based Imports
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed

# User Based Imports
from flask_login import current_user
from models import User


class User_LoginForm(FlaskForm):
    email = StringField('User Email', validators=[DataRequired(), Email()])
    password = PasswordField('User Password', validators=[DataRequired()])
    submit = SubmitField('User Login')


class User_RegistrationForm(FlaskForm):
    email = StringField('User Email', validators=[DataRequired(),Email()])
    username = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('User Password', validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords Must Match!')])
    pass_confirm = PasswordField('Confirm User Password', validators=[DataRequired()])
    admin_consent = RadioField("I consent to admin control", choices=[(0,'admin')])
    submit = SubmitField('User Register')

    def validate_email(self, field):
        # Check if not None for that user email!
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already!')

    def validate_username(self, field):
        # Check if not None for that username!
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Sorry, that username is taken!')


class User_UpdateForm(FlaskForm):
    email = StringField('User Email', validators=[DataRequired(),Email()])
    username = StringField('User Name', validators=[DataRequired()])
    picture = FileField('Update User Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('User Update')

    def validate_email(self, field):
        # Check if not None for that user email!
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already!')

    def validate_username(self, field):
        # Check if not None for that username!
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Sorry, that username is taken!')