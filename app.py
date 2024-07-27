from setup import app
from flask import render_template

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

from user_site.user_blog_post.views import user_blog_post_bp
from user_site.user_authentication.views import user_authentication_bp
from admin_site.admin_blog_post.views import admin_blog_post_bp
from admin_site.admin_authentication.views import admin_authentication_bp
from error_handlers import error_pages_bp

app.register_blueprint(user_blog_post_bp)
app.register_blueprint(user_authentication_bp)
app.register_blueprint(admin_blog_post_bp)
app.register_blueprint(admin_authentication_bp)
app.register_blueprint(error_pages_bp)

if __name__ == '__main__':
    app.run(debug=True) 