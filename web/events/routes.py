"""
This module defines the routes for the events blueprint.
"""

import random
from flask import render_template
from uuid import uuid4

from web.events import events_bp
from models import storage
from models.enum_model import EventStatus, EventLocationType
from models.event import Event
from models.event_category import EventCategory


@events_bp.route("/", strict_slashes=False)
def index():

    # events
    events = storage.all(Event).values()
    events = list(events)[:12]

    # event categories
    event_categories = list(storage.all(EventCategory).values())

    # event status
    event_statuses = sorted(EventStatus, key=lambda x: x.value, reverse=True)

    # event locations
    event_locations = sorted(
        EventLocationType, key=lambda x: x.value, reverse=True)

    return render_template(
        "events/index.html",
        events=events,
        event_categories=event_categories,
        event_statuses=event_statuses,
        event_locations=event_locations,
        title="Events",
        cache_id=uuid4(),
    )
