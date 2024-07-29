from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from setup import db
from werkzeug.security import generate_password_hash,check_password_hash
from models import Admin
from admin_site.admin_authentication.forms import Admin_RegistrationForm, Admin_LoginForm, Admin_UpdateForm
from picture_handler import add_profile_pic
from reauthentication import reauth_required


admin_authentication_bp = Blueprint('admin_authentication_bp', __name__, template_folder = '../templates')

# @admin_authentication_bp.route('/admin_register', methods=['GET', 'POST'])
# def admin_register():
#     form = Admin_RegistrationForm()

#     if form.validate_on_submit():
#         user = Admin(email=form.email.data,
#                     username=form.username.data,
#                     password=form.password.data)

#         db.session.add(user)
#         db.session.commit()
#         flash('Thanks for registering! Now you can login!')
#         return redirect(url_for('admin_authentication_bp.admin_login'))
#     return render_template('admin_register.html', form=form)

@admin_authentication_bp.route('/admin_login', methods=['GET', 'POST'])
def admin_login():

    form = Admin_LoginForm()
    if form.validate_on_submit():
        # Grab the user from our User Models table
        user = Admin.query.filter_by(email=form.email.data).first()

        # Check that the user was supplied and the password is right
        # The verify_password method comes from the User object
        # https://stackoverflow.com/questions/2209755/python-operation-vs-is-not

        if user is not None and user.check_password(form.password.data):
            #Log in the user

            login_user(user)
            flash('Logged in successfully.')

            # If a user was trying to visit a page that requires a login
            # flask saves that URL as 'next'.
            next = request.args.get('next')

            # So let's now check if that next exists, otherwise we'll go to
            # the welcome page.
            if next == None or not next[0]=='/' or next == '/user_logout' or next == '/user_account' or next == '/user_create_post' or next == '/user_read_post/<int:blog_post_id>' or next == '/user_update_post/<int:blog_post_id>' or next == '/user_delete_post/<int:blog_post_id>' or next == '/user_post_list':
                next = url_for('admin_blog_post_bp.admin_post_list')

            return redirect(next)
    return render_template('admin_login.html', form=form)




@admin_authentication_bp.route("/admin_logout")
@login_required
@reauth_required('user')
def admin_logout():
    logout_user()
    return redirect(url_for('home'))


@admin_authentication_bp.route("/admin_account", methods=['GET', 'POST'])
@login_required
@reauth_required('user')
def admin_account():

    form = Admin_UpdateForm()

    if form.validate_on_submit():
        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data,username)
            current_user.profile_image = pic

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('User Account Updated')
        return redirect(url_for('admin_authentication_bp.admin_account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for('static', filename='profile_pics/' + current_user.profile_image)
    return render_template('admin_account.html', profile_image=profile_image, form=form)



