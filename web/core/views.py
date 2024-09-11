"""
This module defines the routes for the core module.
"""

import random
from flask import abort, make_response, render_template, send_from_directory, url_for, current_app
from uuid import uuid4

from web.core import core_bp
from models import storage
from models.event import Event

# define favicon route
def get_favicorn():
    if current_app.static_folder is not None:
        return send_from_directory(
            current_app.static_folder,
            path='images/base_logo.png'
        )
    abort(404)


core_bp.add_url_rule(
    "/favicon.ico", view_func=get_favicorn)


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
