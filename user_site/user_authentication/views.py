from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from setup import db
from werkzeug.security import generate_password_hash,check_password_hash
from models import User
from user_site.user_authentication.forms import User_RegistrationForm, User_LoginForm, User_UpdateForm
from picture_handler import add_profile_pic
from reauthentication import reauth_required


user_authentication_bp = Blueprint('user_authentication_bp', __name__, template_folder = '../templates')

@user_authentication_bp.route('/user_register', methods=['GET', 'POST'])
def user_register():
    form = User_RegistrationForm()

    if form.validate_on_submit():
        admin_id = request.form.get('admin_consent')
        if admin_id == None:
            return render_template('user_register.html', form=form)

        user = User(id=User.get_next_id(),
                    email=form.email.data,
                    username=form.username.data,
                    password=form.password.data,
                    admin_id = int(admin_id))

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering! Now you can login!')
        return redirect(url_for('user_authentication_bp.user_login'))
    return render_template('user_register.html', form=form)

@user_authentication_bp.route('/user_login', methods=['GET', 'POST'])
def user_login():

    form = User_LoginForm()
    if form.validate_on_submit():
        # Grab the user from our User Models table
        user = User.query.filter_by(email=form.email.data).first()

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
            if next == None or not next[0]=='/' or next == '/admin_logout' or next == '/admin_account' or next == '/admin_create_post' or next == '/admin_read_post/<int:blog_post_id>' or next == '/admin_update_post/<int:blog_post_id>' or next == '/admin_delete_post/<int:blog_post_id>' or next == '/admin_post_list' or next == '/admin_user_list' or next == '/admin_deletes_user':
                next = url_for('user_blog_post_bp.user_post_list')

            return redirect(next)
    return render_template('user_login.html', form=form)




@user_authentication_bp.route("/user_logout")
@login_required
@reauth_required('admin')
def user_logout():
    logout_user()
    return redirect(url_for('home'))


@user_authentication_bp.route("/user_account", methods=['GET', 'POST'])
@login_required
@reauth_required('admin')
def user_account():
    details_update = User.query.get(current_user.id)
    form = User_UpdateForm()

    if form.validate_on_submit():
        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data,username)
            details_update.profile_image = pic

        details_update.username = form.username.data
        details_update.email = form.email.data
        db.session.commit()
        flash('User Account Updated')
        return redirect(url_for('user_authentication_bp.user_account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for('static', filename='profile_pics/' + current_user.profile_image)
    return render_template('user_account.html', profile_image=profile_image, form=form)



