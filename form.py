from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, EqualTo, Email, Length
from flask_wtf.file import FileRequired, FileAllowed

class RegistrationForm(FlaskForm):
    username = StringField("Username", [Length(min=4, max=30)], render_kw={"placeholder": "Username"})
    email = StringField("Email", [Length(min=4, max=90), Email()], render_kw={"placeholder": "name@example.com"})
    password = PasswordField("Password", validators=[DataRequired()], render_kw={"placeholder": "Create password"})
    confirm = PasswordField("Confirm", validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "Confirm password"})
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()], render_kw={"placeholder": "name@example.com"})
    password = PasswordField("Password", validators=[DataRequired()], render_kw={"placeholder": "Create password"})
    submit = SubmitField("Login")

class ContactForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()], render_kw={"placeholder": "name@example.com"})
    subject = StringField("Subject", validators=[DataRequired(), Length(min=4, max=100)], render_kw={"placeholder": "Your subject"})
    content = TextAreaField("Message", validators=[DataRequired(), Length(min=4)], render_kw={"placeholder": "Leave a message..."})
    send = SubmitField('Send message')

class ProjectForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=4, max=100)], render_kw={"placeholder": "Project title"})
    description = TextAreaField("Description", validators=[DataRequired()], render_kw={"placeholder": "Project description"})
    image = FileField('Upload image', validators=[FileRequired(), FileAllowed(['jpeg', 'jpg', 'png'], 'Only images allowed!')])
    github_url = StringField("GitHub URL", validators=[DataRequired()], render_kw={"placeholder": "https://github_url_here"})
    demo_url = StringField("Live Demo URL", validators=[DataRequired()], render_kw={"placeholder": "https://live_project_url_here"})
    submit = SubmitField('Submit')