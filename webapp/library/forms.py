from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import SubmitField, StringField, PasswordField, TextAreaField
from wtforms.validators import Required, EqualTo, Email, DataRequired
from .models import *

class FormLogin(FlaskForm):
    Email = StringField("Email", validators=[Required("Type your email"), Email()])
    Password = PasswordField("Password", validators=[Required("Type your password")])
    Login = SubmitField("Log In")


class FormSignup(FlaskForm):
    Name = StringField("Full Name", validators=[Required("Type your full name")])
    Username = StringField("Username", validators=[Required("Type your username")])
    Email = StringField("Email", validators=[Required("Type your email"), Email()])
    Password = PasswordField(
        "Password",
        validators=[
            Required("Type your password"),
            EqualTo("Confirm", message="Passwords must match"),
        ],
    )
    Confirm = PasswordField("Confirm Password")
    Phone = StringField("Phone", validators=[Required("Type your phone number")])
    Address = StringField("Address", validators=[Required("Type your Address")])
    Signup = SubmitField("Sign Up")


class FormContact(FlaskForm):
    Name = StringField("Name", validators=[Required("Type your full name")])
    Email = StringField("Email", validators=[Required("Type your email"), Email()])
    Subject = StringField("Subject", validators=[Required("Type subject")])
    Details = CKEditorField("Details", validators=[Required("Type details")])
    Submit = SubmitField("Submit Now")


class FormAdminLogin(FlaskForm):
    Username = StringField("Username", validators=[Required("Type admin username")])
    Password = PasswordField(
        "Password", validators=[DataRequired("Type admin password")]
    )
    Login = SubmitField("Log In")
