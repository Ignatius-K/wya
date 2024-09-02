"""
This moduled defines the Flask factory function.
"""

import os
from flask import Flask
from helpers import config


def create_app():
    """
    Create and configure a Flask application instance.
    """
    app = Flask(config.APP_NAME)
    app.config.from_object(config)

    # set the template and static folders
    app.template_folder = os.path.join(os.path.dirname(__file__), "templates")
    app.static_folder = os.path.join(os.path.dirname(__file__), "static")

    # initalize the flask plugins

    # register blueprints
    from web.events import events_bp
    from web.core import core_bp
    from web.auth import auth_bp

    app.register_blueprint(core_bp, url_prefix="/")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(events_bp, url_prefix="/events")

    @app.teardown_appcontext
    def close_session(_):
        """
        Close the session after each request.
        """
        from models import storage
        storage.close()

    return app
