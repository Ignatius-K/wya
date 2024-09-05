"""
This module contains the base of the web application.
"""

from flask import Blueprint


core_bp = Blueprint("core", __name__)

# fmt: off
from web.core.views import *

# fmt: on
