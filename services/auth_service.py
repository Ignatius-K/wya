"""
This module handles the authentication of users

Includes:
- Login
- Logout
- Register
- Forgot Password
- Reset Password
"""

from models import storage
from models.user import User
from helpers.password_helper import PasswordManager
from models.enum_model import UserRole


class AuthService:
    """
    This class handles the authentication of users

    Attributes:
        password_manager (PasswordManager): The password manager

    """

    password_manager = PasswordManager()

    @classmethod
    def validate_email(cls, email: str) -> bool:
        """
        Validates the email
        """
        user = storage.query(User, email=email).first()
        return user is not None

    @classmethod
    def login(cls, email: str, password: str) -> User:
        """
        Logs in a user
        """
        user_with_email: User | None = storage.query(
            User, email=email).first()
        if not user_with_email:
            raise ValueError("Check your credentials")
        if not cls.password_manager.verify_password(password, user_with_email.password):
            raise ValueError("Check your credentials")
        return user_with_email

    @classmethod
    def register_user(cls, user_data: dict) -> User | None:
        """
        Creates a user in database

        Params:
            user_data (dict): The user details

        Return:
            (User|None): The user on successful registration else None
        """
        user = User(**user_data)
        if not user.email:
            raise ValueError('Email is required.')

        # check if user exists
        if cls.validate_email(user.email):
            raise ValueError("Account linked to email already exists.")

        # clean user data
        user.first_name: str = user.first_name.capitalize().strip()
        user.last_name: str = user.last_name.capitalize().strip()
        user.password = cls.password_manager.hash_password(
            user.password.strip())

        # set user role
        user.role = UserRole.USER
        try:
            user.save()
            return user
        except Exception as e:
            print(e)
            return None
