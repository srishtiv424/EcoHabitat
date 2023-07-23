from flask_wtf import FlaskForm
from wtforms import  StringField,IntegerField,TextAreaField,SubmitField,PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from .models import User


class NewChallenge(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField("Add Description", validators=[DataRequired()])
    points = IntegerField("Points", validators=[DataRequired()])
    duration = IntegerField("Duration (Days)", validators=[DataRequired()])
    submit = SubmitField("Add Challenge")


class Registration(FlaskForm):
    username = StringField("Enter the username ", validators=[DataRequired()])
    email = StringField("Enter the email", validators=[DataRequired(), Email()])
    password = PasswordField("Enter the password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username already taken")

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError("This email is already registered.")


class Login(FlaskForm):
    email = StringField("Enter the email", validators=[DataRequired(), Email()])
    password = PasswordField("Enter the password", validators=[DataRequired()])
    submit = SubmitField("Login")
