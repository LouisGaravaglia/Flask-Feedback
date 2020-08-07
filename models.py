from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class Pet(db.Model):
    """Creating a Model for our Pet."""

    __tablename__ = "pets"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.Text,
                     nullable=False)
    species = db.Column(db.Text, nullable=True)
    photo = db.Column(db.Text)
    age = db.Column(db.Integer)
    notes = db.Column(db.Text)
    available = db.Column(db.Boolean, nullable=False, default=True)

# class User(db.Model):
#     """Creating a Model for our User."""

#     __tablename__ = "users"

#     id = db.Column(db.Integer,
#                    primary_key=True,
#                    autoincrement=True)
#     username = db.Column(db.Text,
#                      nullable=False, length=20)
#     password = db.Column(db.Text, nullable=False)
#     email = db.Column(db.Text, nullable=False, length=50)
#     first_name = db.Column(db.Text,
#                      nullable=False, length=30)
#     last_name = db.Column(db.Text,
#                      nullable=False, length=30)

    
#     def serialize(self):
#         return {
#             'id': self.id,
#             'username': self.username,
#             'password': self.password,
#             'email': self.email,
#             'first_name': self.first_name,
#             'last_name': self.last_name
#         }