"""
This module defines the routes for the core module.
"""

import random
from flask import render_template
from uuid import uuid4

from web.core import core_bp
from models import storage
from models.event import Event

# define favicon route
core_bp.add_url_rule("/favicon.ico", "favicon",
                     redirect_to="/static/images/base_logo.png")


@core_bp.route("/")
def index():
    events = storage.all(Event).values()
    featured_events = random.sample(list(events), 4)
    main_event = get_main_event()
    return render_template(
        "index.html",
        featured_events=featured_events,
        main_event=main_event,
        cache_id=uuid4()
    )


def get_main_event():
    events = storage.all(Event).values()
    # randomize the events
    main_event = random.choice(list(events))
    return main_event
