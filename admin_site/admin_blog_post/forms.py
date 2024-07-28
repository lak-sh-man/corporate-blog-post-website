from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email


class Admin_BlogPostForm(FlaskForm):
    # no empty titles or text possible
    # we'll grab the date automatically from the Model later
    title = StringField('Admin Title', validators=[DataRequired()])
    text = TextAreaField('Admin Text', validators=[DataRequired()])
    submit = SubmitField('Admin BlogPost')


class Admin_UserDeleteForm(FlaskForm):
    id = IntegerField('Client Id')
    submit = SubmitField('Remove Client')
