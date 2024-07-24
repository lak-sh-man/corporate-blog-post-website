from flask import render_template, request, Blueprint

user_blog_display_bp = Blueprint('user_blog_display_bp', __name__, template_folder = '../templates')

@user_blog_display_bp.route('/user_blog_display')
def user_blog_display():
    '''
    This is the home page view. Notice how it uses pagination to show a limited
    number of posts by limiting its query size and then calling paginate.
    '''
    return render_template('user_blog_display.html')

