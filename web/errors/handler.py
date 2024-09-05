"""
This module defines the handlers
"""

from flask import render_template, redirect, url_for
from flask_wtf.csrf import CSRFError

from web.errors import errors_bp


@errors_bp.app_errorhandler(500)
def internal_server_error(error):
    """
    Render the 500 page.
    """
    return render_template("errors/500.html"), 500


@errors_bp.app_errorhandler(404)
def handle_404(error):
    """
    Render the 404 page.
    """
    return render_template("errors/404.html"), 404


@errors_bp.app_errorhandler(CSRFError)
def handle_expired_csrf(error):
    """
    Render the 403 page.
    """
    return redirect(url_for("events.index"))
