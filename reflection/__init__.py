from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from reflection.users.forms import RegisterForm, LoginForm

from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, current_user, login_required


app = Flask(__name__)
app.config['SECRET_KEY'] = '122c5e10d62545e72aae5a0192d0f269'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt()
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


from reflection.models import User

reflects = [
    {
        'author': 'Gunjan Kaphle',
        'reflect': 'This is me sharing my thoughts for the first time',
        'date_posted': 'Apr 20, 2019'
    },
    {
        'author': 'Test User',
        'reflect': 'So much stuff in here',
        'date_posted': 'Jun 7, 2022'
    }
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', reflects=reflects, title="Home")


@app.route('/about')
def about():
    return render_template('about.html', title="About")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('User created. You can now login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title="Register", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, login_form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Cannot Login. Please try again!', 'danger')
    return render_template('login.html', title='Login', form=login_form)


@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('home'))


@login_required
@app.route('/profile', methods=['GET'])
def account():
    return render_template('profile.html', title='Profile')


if __name__ == '__main__':
    app.run(port=5001, debug=True)
