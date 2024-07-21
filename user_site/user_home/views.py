from flask import render_template, request, Blueprint

user_core = Blueprint('user_core', __name__, template_folder = '../templates')

@user_core.route('/user_home')
def home():
    '''
    This is the home page view. Notice how it uses pagination to show a limited
    number of posts by limiting its query size and then calling paginate.
    '''
    return render_template('users_home.html')

