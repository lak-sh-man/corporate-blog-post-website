from flask import Flask, render_template

app = Flask(__name__, template_folder='templates')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

from user_site.user_home.views import user_core
app.register_blueprint(user_core)

if __name__ == '__main__':
    app.run(debug=True)