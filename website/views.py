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
    return render_template('home.html')

@views.route('/profile')
@login_required
def profile():
    return render_template('profile.html')
