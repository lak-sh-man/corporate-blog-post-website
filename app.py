from flask import Flask, render_template

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    '''
    Example view of any other "core" page. Such as a info page, about page,
    contact page. Any page that doesn't really sync with one of the models.
    '''
    return render_template('about.html')

from user_site.user_home.views import user_core
app.register_blueprint(user_core)

if __name__ == '__main__':
    app.run(debug=True)