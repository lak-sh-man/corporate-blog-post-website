from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from setup import db
from werkzeug.security import generate_password_hash,check_password_hash
from models import User, UserBlogPost
from user_site.user_authentication.forms import User_RegistrationForm, User_LoginForm, User_UpdateForm
from user_site.user_authentication.picture_handler import add_profile_pic


user_authentication_bp = Blueprint('user_authentication_bp', __name__, template_folder = '../templates')

@user_authentication_bp.route('/user_register', methods=['GET', 'POST'])
def user_register():
    form = User_RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

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
            if next == None or not next[0]=='/':
                next = url_for('user_blog_post_bp.user_post_list')

            return redirect(next)
    return render_template('user_login.html', form=form)




@user_authentication_bp.route("/user_logout")
def user_logout():
    logout_user()
    return redirect(url_for('home'))


@user_authentication_bp.route("/user_account", methods=['GET', 'POST'])
@login_required
def user_account():

    form = User_UpdateForm()

    if form.validate_on_submit():
        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data,username)
            current_user.profile_image = pic

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('User Account Updated')
        return redirect(url_for('user_authentication_bp.user_account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for('static', filename='profile_pics/' + current_user.profile_image)
    return render_template('user_account.html', profile_image=profile_image, form=form)


@user_authentication_bp.route("/<username>")
def user_paginate(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    blog_posts = UserBlogPost.query.filter_by(author=user).order_by(UserBlogPost.date.desc()).paginate(page=page, per_page=5)
    return render_template('user_paginate.html', blog_posts=blog_posts, user=user)
