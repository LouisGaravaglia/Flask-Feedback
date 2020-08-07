from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField
from wtforms.validators import InputRequired, Optional, NumberRange, URL, AnyOf, Length, Email



    # username - a unique primary key that is no longer than 20 characters.
    # password - a not-nullable column that is text
    # email - a not-nullable column that is unique and no longer than 50 characters.
    # first_name - a not-nullable column that is no longer than 30 characters.
    # last_name - a not-nullable column that is no longer than 30 characters.


class AddUserForm(FlaskForm):
    """Form for registering new users."""
    
    username = StringField("Username", validators=[Length(min=0, max=20, message="Username can't be more than 30 characters.")])
    password = StringField("Species of Pet")
    email = StringField("Username", validators=[Length(min=0, max=50, message="An email can't be more than 50 characters.")])
    first_name = StringField("Username", validators=[Length(min=0, max=30, message="A first name can't be more than 30 characters.")])
    last_name = StringField("Username", validators=[Length(min=0, max=30, message="A last name can't be more than 30 characters.")])
    


