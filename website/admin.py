from flask import Blueprint, Response
from .models import *

admin = Blueprint('admin', __name__)

@admin.route('/')
def index():
    return 