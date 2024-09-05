"""
Setup the login manager.
"""

from flask_login import LoginManager
from models import storage
from models.user import User


def setup_login_manager(login_manager: LoginManager):
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please login to access this page."
    login_manager.login_message_category = "info"

    @login_manager.user_loader
    def load_user(user_id):
        """
        Gets user from database

        Params:
            user_id (str): ID of the user

        Return:
            (User | None): User if user exists else None
        """
        return storage.get(User, user_id)
