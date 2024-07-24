from setup import app
from flask import render_template

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

from user_site.user_blog_display.views import user_blog_display_bp
from user_site.user_login.views import user_login_bp
from error_handlers import error_pages_bp

app.register_blueprint(user_blog_display_bp)
app.register_blueprint(user_login_bp)
app.register_blueprint(error_pages_bp)

if __name__ == '__main__':
    app.run(debug=True)