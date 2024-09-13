# imports
import os
from flask import Flask, url_for
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()

def create_app():
    # App.py
    app = Flask(__name__)

    # Config
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sparkletheweb.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['UPLOAD_FOLDER'] = 'static/images'
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/images')

    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    login_manager.login_view = "admin.login"


    # Register Bluprints
    from admin import admin as admin_blueprint
    from blog import blog as blog_blueprint

    app.register_blueprint(admin_blueprint,url_prefix ='/admin')
    app.register_blueprint(blog_blueprint)
    
    return app
