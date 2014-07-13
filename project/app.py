import os
import sqlite3
from flask import g, Flask, session, render_template, flash, request, redirect, url_for
from flask.ext.login import LoginManager, login_user, logout_user, login_required
from models import User
from models import db
from werkzeug.contrib.fixers import ProxyFix
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.secret_key = 'Super secret key'

login_manager = LoginManager()
login_manager.init_app(app)

db_session = db.session

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

def load_user_info():
    if session.get('user_id'):
	user = User.query.filter(username=session['user_id']).first()
    else:
	user = None
    g.user = user

@login_manager.user_loader
def load_user(userid):
    try:
	return User.query.get(userid)
    except:
	return None    
    return None

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
	login_user(form.user)
	flash("Logged in succesfully")
	return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
	user = User(form.username.data, form.email.data, form.password.data)
	db_session.add(user)
	db_session.commit()
	flash('Thanks for registering')
	return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route("/dashboard")
@login_required
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
    app.run(port=8080)

