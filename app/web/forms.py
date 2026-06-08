from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError
import re


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[
        DataRequired(),
        Length(min=3, max=50)
    ])
    password = PasswordField("Password", validators=[
        DataRequired(),
        Length(min=6)
    ])
    submit = SubmitField("Register")

    def validate_username(self, field):
        if not re.match(r"^[a-zA-Z0-9_]+$", field.data):
            raise ValidationError("Username can only contain letters, numbers and underscore")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class RecommendForm(FlaskForm):
    text = TextAreaField("Description of a book you liked", validators=[
        DataRequired(),
        Length(min=5, max=1000)
    ])
    submit = SubmitField("Find similar books")