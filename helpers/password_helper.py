"""
This module contains all methods related to password
"""

import bcrypt


class PasswordManager:
    """
    Defines the Password manager class
    where everything related to managing password is handled

    Note:
        This class is a singleton class
        For more information about the singleton pattern, check out:
        https://en.wikipedia.org/wiki/Singleton_pattern
        https://realpython.com/python-singletons/
    """

    __instance = None

    def __new__(cls):
        """
        Creates a new instance of the PasswordManager class
        """
        if cls.__instance is None:
            cls.__instance = super(PasswordManager, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        pass

    def hash_password(self, password: str) -> tuple[str, str]:
        """
        Hashes the password
        """
        encoded_password = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(encoded_password, salt)
        return hashed_password.decode('utf-8')

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """
        Verifies the password
        """
        encoded_password = password.encode('utf-8')
        encoded_hashed_password = hashed_password.encode('utf-8')
        return bcrypt.checkpw(encoded_password, encoded_hashed_password)
