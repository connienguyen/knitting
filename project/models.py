from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import flask.ext.whooshalchemy as whooshalchemy

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://knitsie:knittingiscool!!!@localhost/knitsie'
app.config['WHOOSH_BASE'] = 'search.db'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    __searchable__ = ['username']
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    projects = db.relationship('Project', backref='author', lazy='dynamic')

    def __init__(self, username, email, password):
	self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

    def check_password(self, password):
	return self.password == password

    def is_authenticated(self):
	return True

    def is_anonymous(self):
	return False

    def get_id(self):
	return unicode(self.id)

    def is_active(self):
	return True

class Project(db.Model):
    __tablename__ = 'projects'
    __searchable__ = ['title']
    id = db.Column(db.Integer, primary_key=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    file_path =  db.Column(db.String(120))
    title = db.Column(db.String(120))
    public = db.Column(db.Boolean)   
    across = db.Column(db.Integer)
    tall = db.Column(db.Integer)
    colors = db.Column(db.Integer)
    tags = db.relationship('Tag', backref='project', lazy='dynamic')

    def __init__(self, created_by, file_path, title, public, across, tall, colors):
	self.created_by = created_by
	self.file_path = file_path
	self.title = title
	self.public = public
	self.across = across
	self.tall = tall
	self.colors = colors

    def __repr__(self):
	return '<Project %r>' % self.title

class Tag(db.Model):
    __tablename__ = 'tags'
    __searchable__ = ['tag']
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(80))
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))

    def __init__(self, tag, project_id):
	self.tag = tag
	self.project_id = project_id

    def __repr__(self):
	return '<Tag %r>' % self.tag

whooshalchemy.whoosh_index(app, User)
whooshalchemy.whoosh_index(app, Project)
whooshalchemy.whoosh_index(app, Tag)
