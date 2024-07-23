from flask import render_template, request, Blueprint

user_home_bp = Blueprint('user_home_bp', __name__, template_folder = '../templates')

@user_home_bp.route('/user_home')
def user_home():
    '''
    This is the home page view. Notice how it uses pagination to show a limited
    number of posts by limiting its query size and then calling paginate.
    '''
    return render_template('user_home.html')

