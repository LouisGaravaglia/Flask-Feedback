from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, FloatField
from wtforms.validators import InputRequired, Optional, NumberRange, URL, AnyOf



class AddCupcakeForm(FlaskForm):
    """Form for adding cupcakes."""

    flavor = StringField("Flavor of Cupcake", validators=[InputRequired()])
    size = StringField("Size of Cupcake", validators=[InputRequired()])
    rating = FloatField("Rating of Cupcake", validators=[NumberRange(min=0, max=10, message="The rating must be between 0 and 10."), InputRequired()])
    image = StringField("Photo URL of Cupcake", validators=[URL(require_tld=True, message=None), Optional()])

    


