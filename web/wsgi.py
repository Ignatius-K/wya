"""
This module defines the WSGI entry point
to the web application.
"""

from web import create_app

app = create_app()

if __name__ == "__main__":
    app.run(
        host=app.config["FLASK_HOST"],
        port=app.config["FLASK_PORT"]
    )
