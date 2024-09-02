"""
This module defines the authentication blueprint.
"""

from flask import Blueprint

auth_bp = Blueprint("auth", __name__)

# fmt: off
from web.auth.routes import *

# fmt: on