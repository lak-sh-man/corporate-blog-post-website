from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class Admin_BlogPostForm(FlaskForm):
    # no empty titles or text possible
    # we'll grab the date automatically from the Model later
    title = StringField('Admin Title', validators=[DataRequired()])
    text = TextAreaField('Admin Text', validators=[DataRequired()])
    submit = SubmitField('Admin BlogPost')
