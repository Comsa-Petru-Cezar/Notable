from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from Application.models import User, Note, Tag, File
from flask_login import current_user

class RegForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2,max=20)])
    email = StringField('Email',  validators=[DataRequired(), Email()])
    password = PasswordField('Passward', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Passward', validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign Up')
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists')
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('email already in use')

class LogForm(FlaskForm):
    email = StringField('Email',  validators=[DataRequired(), Email()])
    password = PasswordField('Passward', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')

class NewNote(FlaskForm):
    name = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    tags = StringField('Tag',)
    submit = SubmitField('Create')
    def validate_name(self, name):
        from Application.routes import app
        name = Note.query.filter_by(owner=current_user.id, name=name.data, path=app.current_path).first()


        if name:
            raise ValidationError('Note already exist')

class NewTag(FlaskForm):
    name2 = StringField('Tag Name', validators=[DataRequired()])
    submit = SubmitField('Create Tag')
    def validate_name(self, name2):
        name = Tag.query.filter_by(owner=current_user.id, name=name2.data).first()
        if name:
            raise ValidationError('Tag name already in use')

class NewFile(FlaskForm):
    name1 = StringField('File Name', validators=[DataRequired()])
    submit = SubmitField('Create File')
    def validate_name1(self, name1):
        from Application.routes import app
        name = File.query.filter_by(owner=current_user.id, name=name1.data, path=app.current_path).first()
        print(name,app.current_path)
        if name:
            raise ValidationError('File name already in use')

class EditNote(FlaskForm):
    name = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    tags = StringField('Tag')
    submit = SubmitField('Done')

