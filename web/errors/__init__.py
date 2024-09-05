"""
This module defines the error blueprint
"""

from flask import Blueprint

errors_bp = Blueprint("errors", __name__)

# fmt: off
from .handler import *

# fmt:on