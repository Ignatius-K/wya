"""
This module defines the routes in the authentication blueprint.
"""

from flask_login import login_user, logout_user
from flask import render_template, flash, \
    session, redirect, url_for, request

from web.auth import auth_bp
from .forms import LoginForm, RegisterForm
from services import AuthService
from models.user import User
from helpers.validate import url_has_allowed_host_and_scheme


@auth_bp.route("/login", methods=["GET", "POST"], strict_slashes=False)
def login():
    """
    Render the login page.
    """
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = AuthService.login(form.email.data, form.password.data)
            user_authentication_status = login_user(user)
            if user_authentication_status:
                flash("You have been logged in successfully.", "success")
                # get next and valdate it
                next_page = request.args.get('next')
                if next_page and url_has_allowed_host_and_scheme(next_page, request.host):
                    return redirect(next_page)
                return redirect(url_for("events.index"))
            else:
                flash(
                    "User account is not active. An email has been sent to you to activate your account.", "error")
        except ValueError as e:
            flash("Please check your credentials and try again.", "error")
    return render_template(
        "auth/login.html",
        title="Login",
        form=form
    )


@auth_bp.route("/register", methods=["GET", "POST"], strict_slashes=False)
def register():
    """
    Render the register page.
    """
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            user: User | None = AuthService.register_user(form.data)
            if not user:
                flash('User registration was not successful.', 'error')
            else:
                flash('User registration was successful.', 'success')
                return redirect(url_for('auth.login'))
        except Exception as e:
            flash(str(e), 'error')

    return render_template(
        "auth/register.html",
        title="Register",
        form=form
    )


@auth_bp.route("/logout", methods=["GET"], strict_slashes=False)
def logout():
    """
    Logout the user.
    """
    logout_user()
    flash("You have been logged out successfully.", "success")
    return redirect(url_for("core.index"))
