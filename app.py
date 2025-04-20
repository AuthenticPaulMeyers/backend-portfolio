from flask import flash, Flask, render_template, url_for, redirect, request
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from config import Config
from models import db, Project, User
from werkzeug.security import generate_password_hash, check_password_hash
from form import RegistrationForm
from flask_wtf import CSRFProtect

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
    return render_template('index.html', title="Home")

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
        elif len(username) < 2:
            flash('Username is too short.', category='error')
        else:
            password_hash = generate_password_hash(password)

            user = User(username=username, email=email, password=password_hash)
            db.session.add(user)
            db.session.commit()

        flash('User registered!', category='success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title='Register')

# render login page

# render projects page

# render contact page


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Creates database tables
    app.run(debug=True)