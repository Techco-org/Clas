from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from . import db
from .models import User, Task
from datetime import datetime
import json

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template('home.html' , user=current_user)

@views.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@views.route('/profile/edit-personal', methods=['GET', 'POST'])
@login_required
def edit_personal():
    if request.method == 'POST':
        current_user.fullname = request.form.get('name')
        current_user.bio = request.form.get('bio')
        current_user.city = request.form.get('city')
        current_user.country = request.form.get('country')
        current_user.url = request.form.get('url')
        db.session.commit()
        return redirect(url_for('views.profile'))