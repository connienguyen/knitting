from wtforms import Form, IntegerField, BooleanField, FileField, TextField, PasswordField, validators
from models import User

ALLOWED_IMG_EXT = set(['png', 'jpg', 'jpeg'])

def checkfile(form, field):
    print "image is " + form.image.data
    print "field.data is " + field.data.lower()
    #filename = field.data
    #ext = filename.rsplit('.', 1)[1]
    #print 'upload file extension: ' + ext
    #if not ext.lower() in ALLOWED_IMG_EXT:
    #	raise validators.ValidationError('File must be an image.')

class SearchForm(Form):
    search = TextField('search', [validators.Required()])

class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=25)])
    email = TextField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.Required(),
	validators.Length(min=8, max=100),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.Required()])

class LoginForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [validators.Required()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = User.query.filter_by(
            username=self.username.data).first()
        if user is None:
            self.username.errors.append('Unknown username')
            return False

        if not user.check_password(self.password.data):
            self.password.errors.append('Invalid password')
            return False

        self.user = user
	return True

class UploadForm(Form):
    image = FileField('Image File', [checkfile])
    stitches = IntegerField('Stitches across', [
	    validators.Required(),
	    validators.NumberRange(min=4, max=300, message="Number of stitches across must be between 4 and 300")])
    maxColors = IntegerField('Maximum colors used (Default is 256)', [
	    validators.Optional(), 
	    validators.NumberRange(min=2, max=256, message="Number of colors must be between 2 and 256.")])
    title = TextField('Project Title', [validators.Length(min=2, max=120)])
    public = BooleanField('Make public?')
    tags = TextField('Tags - seperate tags using commas', [validators.Optional(), validators.Length(max=128)])

class EditProjectForm(Form):
    title = TextField('Project Title', [validators.Optional(), validators.Length(min=2, max=120)])
    tags = TextField('Tags: separate tags using commas', [validators.Optional()])
    status = BooleanField('Change status?')
