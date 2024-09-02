"""
This module defines the routes in the authentication blueprint.
"""

from flask import render_template, request, redirect, url_for
from web.auth import auth_bp


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Render the login page.
    """
    if request.method == "POST":
        return redirect(url_for("core.index"))
    return render_template(
        "auth/login.html",
        title="Login",
    )


@auth_bp.route("/register")
def register():
    """
    Render the register page.
    """
    return render_template(
        "auth/register.html",
        title="Register"
    )
