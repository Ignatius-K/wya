"""
This module defines the events blueprint.
"""

from flask import Blueprint

events_bp = Blueprint("events", __name__)

# fmt: off
from .views import *

# fmt: on