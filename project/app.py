from flask import Flask, render_template
from werkzeug.contrib.fixers import ProxyFix
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/logout")
def logout():
    return render_template('logout.html')

@app.route("/signup")
def signup():
    return render_template('signup.html');

@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')

@app.route("/tagged")
def tagged():
    return render_template('tagged.html')

@app.route("/project")
def project():
    return render_template('project.html')

@app.route("/upload")
def upload():
    return render_template('upload.html')

app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == '__main__':
    app.debug = True
    app.run()

