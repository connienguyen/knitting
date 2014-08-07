import os
import sqlite3
from datetime import datetime
from flask import g, Flask, session, render_template, flash, request, redirect, url_for
from flask.ext.login import LoginManager, current_user, login_user, logout_user, login_required
from models import User, Project, Tag
from models import db
from werkzeug.contrib.fixers import ProxyFix
from werkzeug.utils import secure_filename
from forms import SearchForm, RegistrationForm, LoginForm, UploadForm, EditProjectForm
from pattern import processImage

BASEDIR = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = BASEDIR + '/uploads/'
IMG_EXTS = ['jpg', 'jpeg', 'png']
POSTS_PER_PAGE = 10
MAX_SEARCH = 25

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

@app.before_request
def before_request():
    g.search_form = SearchForm(request.form)

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

@app.route("/search", methods=['POST'])
def search():
    print "Search query", g.search_form.search.data
    if not g.search_form.validate():
	return redirect(url_for('index'))
    return redirect(url_for('search_results', query=g.search_form.search.data))

@app.route("/search/<query>")
def search_results(query):
    users = User.query.whoosh_search(query, MAX_SEARCH).all()
    projects = Project.query.whoosh_search(query, MAX_SEARCH).filter_by(public=True).all()
    qtags = Tag.query.whoosh_search(query, MAX_SEARCH).all()
    tags = []
    for tag in qtags:
	if tag.tag not in tags:
	    tags.append(tag.tag)
    return render_template('search_results.html', query=query, users=users, projects=projects, tags=tags)

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
@app.route("/dashboard/<int:page>")
@login_required
def dashboard(page=1):
    user_id = session.get('user_id')
    projects = Project.query.filter_by(created_by=user_id).order_by(Project.id.desc()).paginate(page, POSTS_PER_PAGE, False)
    return render_template('dashboard.html', projects=projects)

@app.route("/tagged/<tag>")
@app.route("/tagged/<tag>/<int:page>")
def tagged(tag, page=1):
    tags = Tag.query.filter_by(tag=tag).order_by(Tag.project_id.desc()).paginate(page, POSTS_PER_PAGE, False)
    return render_template('tagged.html', tags=tags, tagged=tag)

@app.route("/project/<pid>")
def project(pid):
    user = User.query.filter_by(id=session.get('user_id')).first()
    project = Project.query.filter_by(id=pid).first()
    if project == None:
	flash('Project not found.')
	return redirect(url_for('index'))
    elif not project.public and user != project.author:
	return redirect(url_for('index'))
    return render_template('project.html', project=project, user=user)

@app.route("/edit/<pid>", methods=['GET', 'POST'])
def editProject(pid):
    project = Project.query.filter_by(id=pid).first()
    user = User.query.filter_by(id=session.get('user_id')).first()
    form = EditProjectForm(request.form)
    if request.method == 'POST' and form.validate():
	if user == project.author:
	    if form.title.data:
		project.title = form.title.data
	    if form.status.data:
		project.public = not project.public
	    if form.tags.data:
		newTags = form.tags.data
		newTags = newTags.split(',')
		oldTags = Tag.query.filter_by(project_id=project.id).all()
		for tag in oldTags:
		    db_session.delete(tag)
		for tag in newTags:
		    tag = Tag(tag.strip(), project.id)
		    db_session.add(tag)
	    db_session.add(project)
	    db_session.commit()
	    return redirect(url_for('project', pid=project.id))
	return redirect(url_for('index'))
    return render_template('edit.html', form=form, project=project)

@app.route("/remove/<pid>")
def removeProject(pid):
    project = Project.query.filter_by(id=pid).first()
    user = User.query.filter_by(id=session.get('user_id')).first()
    if user == project.author:
	for tag in project.tags:
	    db_session.delete(tag)
	db_session.delete(project)
	db_session.commit()
	return redirect(url_for('dashboard'))
    return redirect(url_for('project', pid=project.id))

@app.route("/user/<username>")
@app.route("/user/<username>/<int:page>")
def user(username, page=1):
    currUser = User.query.filter_by(id=session.get('user_id')).first()
    user = User.query.filter_by(username=username).first()
    if user == None:
	flash('User not found.')
	return redirect(url_for('index'))
    else:
	projects = Project.query.filter_by(created_by=user.id).order_by(Project.id.desc()).paginate(page, POSTS_PER_PAGE, False)
	return render_template('user.html', user=user, currUser=currUser, projects=projects)

@app.route("/upload", methods=['GET', 'POST'])
def upload():
    form = UploadForm(request.form)
    if request.method == 'POST' and form.validate():
	image = request.files['image']
	if image:
	    filename = secure_filename(image.filename)
	    filename, ext = filename.split('.', 1)
	    if ext not in IMG_EXTS:
		return redirect(url_for('dashboard'))
	    timestamp = cleanTime(str(datetime.utcnow()))
	    filename = filename + timestamp + '.' + ext
	    image_data = request.files[image.name].read()
	    open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'w').write(image_data)
	    flash('You have uploaded a file')
	    if form.maxColors.data:
		patternfile, across, tall = processImage(filename, form.stitches.data, form.maxColors.data)
		colors = form.maxColors.data
	    else:
		patternfile, across, tall = processImage(filename, form.stitches.data)
		colors = 256
	    os.remove(UPLOAD_FOLDER + filename)
	    patternsave = url_for('static', filename=patternfile)
	    project = Project(session.get('user_id'), patternsave, form.title.data, form.public.data, across, tall, colors) 
	    db_session.add(project)
	    db_session.commit()
	    tags = form.tags.data
	    if tags:
		tags = tags.split(',')
		for tag in tags:
		    if tag != '':
			tag = Tag(tag.strip(), project.id)
			db_session.add(tag)
		db_session.commit()
	    return redirect(url_for('dashboard'))
	return redirect(url_for('index.html'))
    return render_template('upload.html', form = form)

app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == '__main__':
    app.debug = True
    app.run(port=8080)

