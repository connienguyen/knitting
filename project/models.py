from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:data.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))

    def __init__(self, username, email, password):
	self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    file_path =  db.Column(db.String(120))
    title = db.Column(db.String(120))
    public = db.Column(db.Boolean)   

    def __init__(self, created_by, file_path, title, public):
	self.created_by = created_by
	self.file_path = file_path
	self.title = title
	self.public = public

    def __repr__(self):
	return '<Project %r>' % self.title

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(80))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

    def __init__(self, tag, project_id):
	self.tag = tag
	self.project_id = project_id

    def __repr__(self):
	return '<Tag %r>' % self.tag


