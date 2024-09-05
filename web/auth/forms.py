"""
This module defines the forms for the authentication blueprint.
"""

from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired, Regexp, EqualTo, Length


class LoginForm(FlaskForm):
    """
    This class defines the login form.
    """

    email = EmailField(
        "Email",
        render_kw={"placeholder": "Enter your email"},
        validators=[DataRequired()]
    )
    password = PasswordField(
        "Password",
        render_kw={"placeholder": "Enter your password"},
        validators=[DataRequired(), Regexp(
            r"^.{8,}$", message="Password must be at least 8 characters long")]
    )
    submit = SubmitField("Sign In")


class RegisterForm(FlaskForm):
    """This class defines the form for user registration."""

    first_name = StringField(
        "First Name",
        render_kw={"placeholder": "Enter your first name"},
        validators=[DataRequired(), Length(min=3, max=50)]
    )
    last_name = StringField(
        "Last Name",
        render_kw={"placeholder": "Enter your last name"},
        validators=[DataRequired(), Length(min=3, max=50)]
    )
    email = EmailField(
        "Email",
        render_kw={"placeholder": "Enter your email"},
        validators=[DataRequired()]
    )
    password = PasswordField(
        "Password",
        render_kw={"placeholder": "Enter your password"},
        validators=[DataRequired(), Length(max=50), Regexp(
            r"^.{8,}$", message="Password must be at least 8 characters long")]
    )
    confirm_password = PasswordField(
        "Confirm Password",
        render_kw={"placeholder": "Confirm your password"},
        validators=[EqualTo("password", "Password must match")]
    )
