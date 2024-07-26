from flask import render_template, request, Blueprint
from models import UserBlogPost
from flask_login import current_user, login_required

user_blog_post_bp = Blueprint('user_blog_post_bp', __name__, template_folder = '../templates')

@user_blog_post_bp.route('/user_post_list')
@login_required
def user_post_list():
    '''
    This is the home page view. Notice how it uses pagination to show a limited
    number of posts by limiting its query size and then calling paginate.
    '''
    page = request.args.get('page', 1, type=int)
    # blog_posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page, per_page=10)
    blog_posts = UserBlogPost.query.filter_by(user_id=current_user.id).order_by(UserBlogPost.date.desc()).paginate(page=page, per_page=10)
    return render_template('user_post_list.html', blog_posts=blog_posts)