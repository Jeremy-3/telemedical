from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash



db = SQLAlchemy()


class User(db.Model):
    __tablename__ ="users"
    
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(100), nullable=False)
    email=db.Column(db.String, nullable=False,unique=True)
    password_hash=db.Column(db.String(255), nullable=False)
    role=db.Column(db.String(20),nullable=False,default="user")
    is_banned = db.Column(db.Boolean, default=False,nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

# Method to hash password before storing
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Method to convert user object to dictionary
    def to_dict(self):
        return{
            'id':self.id,
            'username':self.username,
            'email':self.email,
            'password_hash': self.password_hash,
            'role':self.role,
            'is_banned':self.is_banned,
            'created_at':self.created_at
            }