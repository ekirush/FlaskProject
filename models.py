from app import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model,UserMixin):
    uid = db.Column(db.Integer, primary_key = True, nullable = False)
    username = db.Column(db.String(150), nullable = False, unique = True )
    password = db.Column(db.String(100), nullable = False)
    
class Article(db.Model):
    aid = db.Column(db.Integer, primary_key = True, nullable = False)
    title = db.Column(db.String(100), nullable = False)
    content = db.Column(db.Text, nullable = False)
    image_file = db.Column(db.String(120), nullable=True)
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    

    
    