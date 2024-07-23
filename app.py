from flask import Flask, render_template

app = Flask(__name__, template_folder='templates')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

from user_site.user_home.views import user_home_bp
from user_site.user_login.views import user_login_bp
from error_handlers import error_pages_bp

app.register_blueprint(user_home_bp)
app.register_blueprint(user_login_bp)
app.register_blueprint(error_pages_bp)

if __name__ == '__main__':
    app.run(debug=True)