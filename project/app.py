import os
import sqlite3
from datetime import datetime
from flask import g, Flask, session, render_template, flash, request, redirect, url_for
from flask.ext.login import LoginManager, current_user, login_user, logout_user, login_required
from models import User, Project
from models import db
from werkzeug.contrib.fixers import ProxyFix
from werkzeug.utils import secure_filename
from forms import RegistrationForm, LoginForm, UploadForm
from pattern import processImage

UPLOAD_FOLDER = os.path.dirname(os.path.realpath(__file__)) + '/uploads/'
SAVED_FOLDER = os.path.dirname(os.path.realpath(__file__)) + '/images/'

app = Flask(__name__)
app.secret_key = 'Super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

login_manager = LoginManager()
login_manager.init_app(app)

db_session = db.session

def cleanTime(timeString):
    x = "- :."
    for i in range(0, len(x)):
	timeString = timeString.replace(x[i], "")
    return timeString

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
    if current_user.is_authenticated():
	return redirect(url_for('dashboard'))
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
    user_id = session.get('user_id')
    projects = Project.query.filter_by(created_by=user_id).all()
    return render_template('dashboard.html', projects=projects)

@app.route("/tagged")
def tagged():
    return render_template('tagged.html')

@app.route("/project")
def project():
    return render_template('project.html')

@app.route("/upload", methods=['GET', 'POST'])
def upload():
    form = UploadForm(request.form)
    if request.method == 'POST' and form.validate():
	image = request.files['image']
	if image:
	    filename = secure_filename(image.filename)
	    filename, ext = filename.split('.', 1)
	    timestamp = cleanTime(str(datetime.now()))
	    filename = filename + timestamp + '.' + ext
	    image_data = request.files[image.name].read()
	    open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'w').write(image_data)
	    flash('You have uploaded a file')
	    if form.maxColors.data:
		patternfile = processImage(filename, form.stitches.data, form.maxColors.data)
	    else:
		patternfile = processImage(filename, form.stitches.data)
	    os.remove(UPLOAD_FOLDER + filename)
	    patternfile = SAVED_FOLDER + patternfile
	    project = Project(session.get('user_id'), patternfile, form.title.data, form.public.data) 
	    db_session.add(project)
	    db_session.commit()
	    return redirect(url_for('dashboard'))
	return render_template('index.html', form = form)
    return render_template('upload.html', form = form)

app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == '__main__':
    app.debug = True
    app.run(port=8080)

