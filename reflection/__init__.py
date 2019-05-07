from flask import Flask, render_template, url_for, flash, redirect
from reflection.users.forms import RegisterForm, LoginForm


app = Flask(__name__)
app.config['SECRET_KEY'] = '122c5e10d62545e72aae5a0192d0f269'

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
        flash('User created. You can now login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title="Register", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        flash('You are now logged in. Start Posting!', 'success')
        return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=login_form)


if __name__ == '__main__':
    app.run(port=5001, debug=True)
