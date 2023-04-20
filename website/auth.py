from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_remembered, current_user, login_required, logout_user
from . import db
from .models import User

auth = Blueprint('auth', __name__)

@auth.route('/')
def index():
    return render_template('index.html')

@auth.route('/login', methods=['GET','POST'])
def login():
    if login_remembered():
        return redirect(url_for('views.home'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember')
        user = User.query.filter_by(email=email).first()
        if user:
            if password == user.password:
                if remember is None:
                    login_user(user, remember=False)
                else:
                    login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else: 
                flash('Incorrect password, try again', category='error')
        else:
            flash('Email does not exist', category='error')
        return redirect(url_for('auth.login'))
    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        password = request.form.get('password')
        reconfirm = request.form.get('reconfirm')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category='error')
        elif len(fullname) < 4:
            flash('Full name is too short', category='error')
        elif len(email) < 4:
            flash('Invalid email', category='error')
        elif len(password) < 8:
            flash('Password is too short', category='error')
        elif password != reconfirm:
            flash('Password don\'t match', category='error')
        else:
            new_user = User(fullname=fullname, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created', category='success')
        return redirect(url_for('auth.signup'))
    return render_template('signup.html')