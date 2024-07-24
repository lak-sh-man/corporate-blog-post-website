from flask import render_template, request, Blueprint

user_blog_post_bp = Blueprint('user_blog_post_bp', __name__, template_folder = '../templates')

@user_blog_post_bp.route('/user_post_list')
def user_post_list():
    '''
    This is the home page view. Notice how it uses pagination to show a limited
    number of posts by limiting its query size and then calling paginate.
    '''
    return render_template('user_post_list.html')