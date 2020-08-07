from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


# class Pet(db.Model):
#     """Creating a Model for our Pet."""

#     __tablename__ = "pets"

#     id = db.Column(db.Integer,
#                    primary_key=True,
#                    autoincrement=True)
#     name = db.Column(db.Text,
#                      nullable=False, )
#     species = db.Column(db.Text, nullable=True)
#     photo = db.Column(db.Text)
#     age = db.Column(db.Integer)
#     notes = db.Column(db.Text)
#     available = db.Column(db.Boolean, nullable=False, default=True)

class User(db.Model):
    """Creating a Model for our User."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)

    @classmethod
    def register(cls, username, pwd, email, first_name, last_name):
        """Register user w/ hased password and return that user."""
        
        hashed = bcrypt.generate_password_hash(pwd)
        hashed_utf8 = hashed.decode("utf8")
        
        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)
    
    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists and the password is correct"""
        
        u = User.query.filter_by(username=username).first()
        
        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        else:
            return False
        
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name
        }