from flask import flash, Flask, render_template, url_for, redirect, request, send_file
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from config import Config
from models import db, Project, User, Message
from werkzeug.security import generate_password_hash, check_password_hash
from form import RegistrationForm, LoginForm, ContactForm, ProjectForm
from flask_wtf import CSRFProtect
from werkzeug.utils import secure_filename
from io import BytesIO

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

csrf = CSRFProtect(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# render home page
@app.route('/')
@app.route('/home')
def home():
    projects = Project.query.all()
    return render_template('index.html', title="Home", projects=projects)

# render registration page
@app.route('/register', methods=['GET', 'POST'])
def register():

    form = RegistrationForm()

    if request.method == 'POST' and form.validate():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

        if email_exists:
            flash('Email is already in use.', category='error')
        elif username_exists:
            flash('Username is already in use.', category='error')
        else:
            password_hash = generate_password_hash(password)

            user = User(username=username, email=email, password=password_hash)
            db.session.add(user)
            db.session.commit()

        flash('User registered successfully!', category='success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title='Register')

# render login page
@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data
        # get data from the users table
        user = User.query.filter_by(email=email).first()
        
        if user is None or not check_password_hash(user.password, password):
            flash("Wrong username or password", category='error')
            return redirect(url_for('login'))
        login_user(user) # let the user be stored into the session container
        return redirect(url_for('dashboard'))
    return render_template('login.html', title='Login', form=form)

# render contact page
@app.route('/contact', methods=['POST', 'GET'])
def contact():
    form = ContactForm()
    if request.method == 'POST' and form.validate():
        email = form.email.data
        subject = form.subject.data
        content = form.content.data

        message = Message(email=email, subject=subject, content=content)
        db.session.add(message)
        db.session.commit()

        flash('Message sent! Thank you for working with me.', category='success')
        return redirect(url_for('contact'))
    return render_template('contact.html', title='Contact', form=form)

# dashboard
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    messages = Message.query.all()
    count_messages = len(messages)

    users = User.query.all()
    count_users = len(users)

    projects = Project.query.all()
    count_projects = len(projects)

    return render_template('dashboard.html', title='Dashboard', name=current_user.username, count_messages=count_messages, count_users=count_users, count_projects=count_projects, users=users, messages=messages, projects=projects)

# log out user
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

# edit user
@app.route('/edit')
@login_required
def edit():
    
    return redirect(url_for('register'))

# delete user
@app.route('/delete')
@login_required
def delete():
    
    return redirect(url_for('dashboard'))

# project upload 
@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_project():

    form = ProjectForm()

    if request.method == 'POST' and form.validate():
        title = form.title.data
        description = form.description.data
        image = form.image.data
        github_url = form.github_url.data
        demo_url = form.demo_url.data

        if image or image.filename != '':
            image_mimetype=image.mimetype
            filename = secure_filename(image.filename)
            image_data = image.read() # Read image is binary data

            project = Project(title=title, image=image_data, image_filename=filename, image_mimetype=image_mimetype, description=description, github_url=github_url, live_demo_url=demo_url)

            db.session.add(project)
            db.session.commit()

            flash('Uploaded successfully!', category='success')
            return redirect(url_for('dashboard'))
        else:
            flash('No file selected.', category='error')
    return render_template('upload_project.html', form=form, title='Upload')

#Retrieve the image route
@app.route('/product_image/<int:project_id>')
def project_image(project_id):
    project = Project.query.filter_by(id=project_id).first()

    if project:
        mimetype = project.image_mimetype or 'image/jpeg'
        download_name = project.image_filename
        return send_file(BytesIO(project.image), mimetype=mimetype, download_name=download_name)
    return "Image not found!", 404


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Creates database tables
    app.run(debug=True)