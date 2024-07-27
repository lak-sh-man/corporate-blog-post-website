from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class User_BlogPostForm(FlaskForm):
    # no empty titles or text possible
    # we'll grab the date automatically from the Model later
    title = StringField('User Title', validators=[DataRequired()])
    text = TextAreaField('User Text', validators=[DataRequired()])
    submit = SubmitField('User BlogPost')
