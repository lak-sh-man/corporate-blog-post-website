from flask import abort, render_template,url_for,flash, redirect,request,Blueprint
from flask_login import current_user,login_required
from setup import db
from models import UserBlogPost
from user_site.user_blog_post.forms import User_BlogPostForm
from flask import render_template, request, Blueprint
from flask_login import current_user, login_required
from reauthentication import reauth_required

user_blog_post_bp = Blueprint('user_blog_post_bp', __name__, template_folder = '../templates')


@user_blog_post_bp.route('/user_create_post', methods=['GET','POST'])
@login_required
@reauth_required('admin')
def user_create_post():
    form = User_BlogPostForm()

    if form.validate_on_submit():

        blog_post = UserBlogPost(title=form.title.data,
                                 text=form.text.data,
                                 user_id=current_user.id)
        db.session.add(blog_post)
        db.session.commit()
        flash("Blog Post Created")
        return redirect(url_for('user_blog_post_bp.user_post_list'))

    return render_template('user_create_post.html',form=form)


# int: makes sure that the blog_post_id gets passed as in integer
# instead of a string so we can look it up later.
@user_blog_post_bp.route('/user_read_post/<int:blog_post_id>')
@login_required
@reauth_required('admin')
def user_read_post(blog_post_id):
    # grab the requested blog post by id number or return 404
    blog_post = UserBlogPost.query.get_or_404(blog_post_id)
    return render_template('user_read_post.html',title=blog_post.title,
                            date=blog_post.date,post=blog_post)

@user_blog_post_bp.route("/user_update_post/<int:blog_post_id>", methods=['GET', 'POST'])
@login_required
@reauth_required('admin')
def user_update_post(blog_post_id):
    blog_post = UserBlogPost.query.get_or_404(blog_post_id)
    if blog_post.user_author != current_user:
        # Forbidden, No Access
        abort(403)

    form = User_BlogPostForm()
    if form.validate_on_submit():
        blog_post.title = form.title.data
        blog_post.text = form.text.data
        db.session.commit()
        flash('Post Updated')
        return redirect(url_for('user_blog_post_bp.user_read_post', blog_post_id=blog_post.id))
    # Pass back the old blog post information so they can start again with
    # the old text and title.
    elif request.method == 'GET':
        form.title.data = blog_post.title
        form.text.data = blog_post.text
    return render_template('user_create_post.html', title='Update', form=form)


@user_blog_post_bp.route("/user_delete_post/<int:blog_post_id>", methods=['POST'])
@login_required
@reauth_required('admin')
def user_delete_post(blog_post_id):
    blog_post = UserBlogPost.query.get_or_404(blog_post_id)
    if blog_post.user_author != current_user:
        abort(403)
    db.session.delete(blog_post)
    db.session.commit()
    flash('Post has been deleted')
    return redirect(url_for('user_blog_post_bp.user_post_list'))


@user_blog_post_bp.route('/user_post_list')
@login_required
@reauth_required('admin')
def user_post_list():
    '''
    This is the home page view. Notice how it uses pagination to show a limited
    number of posts by limiting its query size and then calling paginate.
    '''
    page = request.args.get('page', 1, type=int)
    # blog_posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page, per_page=10)
    blog_posts = UserBlogPost.query.filter_by(user_id=current_user.id).order_by(UserBlogPost.date.desc()).paginate(page=page, per_page=10)
    return render_template('user_post_list.html', blog_posts=blog_posts)