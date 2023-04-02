from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_msearch import Search

import tempfile
import os

db = SQLAlchemy()
DB_NAME = "database.db"

search = Search(db=db)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'clas-steam'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONs'] = True
    app.config['MSEARCH_BACKEND'] = 'whoosh'

    from .views import views
    from .auth import auth
    from .data import data

    db.init_app(app)
    search.init_app(app)
    
    from .models import User

    with app.app_context():
        db.create_all()
        search.create_index(User, update=True)

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(data, url_prefix='/data')
    app.register_blueprint(views, url_prefix='/home')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app