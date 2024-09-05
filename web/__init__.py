"""
This moduled defines the Flask factory function.
"""

import os
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager

from helpers import config


# Create plugin instances
csrf = CSRFProtect()
login_manager = LoginManager()


def __register_error_handlers(app):
    """
    Register error handlers for the app.
    """
    from web.errors import errors_bp
    app.register_blueprint(errors_bp)


def __register_blueprints(app):
    """
    Register blueprints for the app.
    """
    from web.events import events_bp
    from web.core import core_bp
    from web.auth import auth_bp

    app.register_blueprint(core_bp, url_prefix="/")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(events_bp, url_prefix="/events")


def __register_plugins(app):
    """
    Register plugins for the app.
    """
    from web.plugins.setup_login import setup_login_manager

    login_manager.init_app(app)
    setup_login_manager(login_manager)

    csrf.init_app(app)


def create_app():
    """
    Create and configure a Flask application instance.
    """
    app = Flask(config.APP_NAME)
    app.config.from_object(config)

    # set the template and static folders
    app.template_folder = os.path.join(os.path.dirname(__file__), "templates")
    app.static_folder = os.path.join(os.path.dirname(__file__), "static")

    __register_plugins(app)
    __register_error_handlers(app)
    __register_blueprints(app)

    @app.teardown_appcontext
    def close_session(_):
        """
        Close the session after each request.
        """
        from models import storage
        storage.close()

    return app
