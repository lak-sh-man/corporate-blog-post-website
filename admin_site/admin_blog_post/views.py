from flask import abort, render_template,url_for,flash, redirect,request,Blueprint
from flask_login import current_user,login_required
from setup import db
from admin_site.admin_blog_post.forms import Admin_BlogPostForm
from flask import render_template, request, Blueprint
from models import AdminBlogPost, User
from flask_login import current_user, login_required

admin_blog_post_bp = Blueprint('admin_blog_post_bp', __name__, template_folder = '../templates')


@admin_blog_post_bp.route('/admin_create_post', methods=['GET','POST'])
@login_required
def admin_create_post():
    form = Admin_BlogPostForm()

    if form.validate_on_submit():

        blog_post = AdminBlogPost(title=form.title.data,
                                 text=form.text.data,
                                 user_id=current_user.id)
        db.session.add(blog_post)
        db.session.commit()
        flash("Blog Post Created")
        return redirect(url_for('admin_blog_post_bp.admin_post_list'))

    return render_template('admin_create_post.html',form=form)


# int: makes sure that the blog_post_id gets passed as in integer
# instead of a string so we can look it up later.
@admin_blog_post_bp.route('/admin_read_post/<int:blog_post_id>')
@login_required
def admin_read_post(blog_post_id):
    # grab the requested blog post by id number or return 404
    blog_post = AdminBlogPost.query.get_or_404(blog_post_id)
    return render_template('admin_read_post.html',title=blog_post.title,
                            date=blog_post.date,post=blog_post)

@admin_blog_post_bp.route("/admin_update_post/<int:blog_post_id>", methods=['GET', 'POST'])
@login_required
def admin_update_post(blog_post_id):
    blog_post = AdminBlogPost.query.get_or_404(blog_post_id)
    if blog_post.admin_author != current_user:
        # Forbidden, No Access
        abort(403)

    form = Admin_BlogPostForm()
    if form.validate_on_submit():
        blog_post.title = form.title.data
        blog_post.text = form.text.data
        db.session.commit()
        flash('Post Updated')
        return redirect(url_for('admin_blog_post_bp.admin_read_post', blog_post_id=blog_post.id))
    # Pass back the old blog post information so they can start again with
    # the old text and title.
    elif request.method == 'GET':
        form.title.data = blog_post.title
        form.text.data = blog_post.text
    return render_template('admin_create_post.html', title='Update', form=form)


@admin_blog_post_bp.route("/admin_delete_post/<int:blog_post_id>", methods=['POST'])
@login_required
def admin_delete_post(blog_post_id):
    blog_post = AdminBlogPost.query.get_or_404(blog_post_id)
    if blog_post.admin_author != current_user:
        abort(403)
    db.session.delete(blog_post)
    db.session.commit()
    flash('Post has been deleted')
    return redirect(url_for('admin_blog_post_bp.admin_post_list'))


@admin_blog_post_bp.route('/admin_post_list')
@login_required
def admin_post_list():
    '''
    This is the home page view. Notice how it uses pagination to show a limited
    number of posts by limiting its query size and then calling paginate.
    '''
    page = request.args.get('page', 1, type=int)
    # blog_posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page, per_page=10)
    blog_posts = AdminBlogPost.query.filter_by(user_id=current_user.id).order_by(AdminBlogPost.date.desc()).paginate(page=page, per_page=10)
    return render_template('admin_post_list.html', blog_posts=blog_posts)

@admin_blog_post_bp.route('/admin_user_list')
@login_required
def admin_user_list():
    clients = User.query.all()
    return render_template('admin_user_list.html', clients=clients)