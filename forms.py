from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, PasswordField
from wtforms.validators import InputRequired, Optional, NumberRange, URL, AnyOf, Length, Email




class AddUserForm(FlaskForm):
    """Form for registering new users."""
    
    username = StringField("Username", validators=[Length(min=0, max=20, message="Username can't be more than 30 characters.")])
    password = PasswordField("Password")
    email = StringField("Email", validators=[Length(min=0, max=50, message="An email can't be more than 50 characters.")])
    first_name = StringField("First Name", validators=[Length(min=0, max=30, message="A first name can't be more than 30 characters.")])
    last_name = StringField("Last Name", validators=[Length(min=0, max=30, message="A last name can't be more than 30 characters.")])




class AddFeedbackForm(FlaskForm):
    """Form for registering new users."""
    
    title = StringField("Title", validators=[Length(min=0, max=100, message="Title can't be more than 100 characters.")])
    content = StringField("Content", validators=[InputRequired()])


