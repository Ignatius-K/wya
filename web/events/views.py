"""
This module defines the routes for the events blueprint.
"""

from uuid import uuid4
from flask import render_template, flash, redirect, url_for, abort, request
from flask_login import login_required, current_user

from web.events import events_bp
from models.event import Event
from models.user import User
from models.enum_model import UserRole
from services import EventService
from .forms import EventForm, EventImageForm


def get_current_user() -> User | None:
    """Returns logged in user"""
    if current_user.is_anonymous or not current_user.is_authenticated:
        return None
    return current_user


@events_bp.route("/", strict_slashes=False)
def index():

    events = EventService.get_all_events()
    event_categories = EventService.get_event_categories()
    event_statuses = EventService.get_event_statuses()
    event_locations = EventService.get_event_locations()

    return render_template(
        "events/index.html",
        events=events,
        event_categories=event_categories,
        event_statuses=event_statuses,
        event_locations=event_locations,
        title="Events",
        cache_id=uuid4(),
    )


@events_bp.route("/mine", strict_slashes=False)
@login_required
def user_events():
    try:
        events = EventService.get_user_events()
    except ValueError as e:
        print(e)
        events = []
    return render_template(
        "events/user_events.html",
        events=events,
        title="My Events",
        hide_footer=True,
        cache_id=uuid4(),
    )


@events_bp.route("/<uuid:event_id>", strict_slashes=False)
def event_details(event_id):
    event: Event = EventService.get_event(event_id)
    if not event:
        abort(404)

    # check whether user already saved the event
    is_owner, is_saved, is_admin = False, False, False
    if current_user.is_authenticated:
        is_owner = EventService.is_event_owner(event_id, current_user.id)
        is_saved = EventService.is_event_saved(event_id, current_user.id)

    logged_in_user = get_current_user()
    if logged_in_user is not None:
        is_admin = get_current_user().role == UserRole.ADMIN

    event_likes = len(event._liked_by)
    return render_template(
        "events/event_details.html",
        title=event.title,
        event=event,
        is_owner=is_owner,
        is_saved=is_saved,
        is_admin=is_admin,
        event_likes=event_likes,
        hide_footer=True,
        cache_id=uuid4(),
    )


@events_bp.route("/create", methods=["GET", "POST"], strict_slashes=False)
@login_required
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        try:
            event = EventService.create_event(form.data)
            if not event:
                flash("Event creation failed", "error")
            else:
                flash(f'Event {event.title} created successfully', "success")
                return redirect(url_for("events.user_events"))
        except ValueError as e:
            flash(e, "error")
    else:
        print(form.errors)
    return render_template(
        "events/create_event.html",
        title="Create Event",
        form=form,
        hide_footer=True,
        cache_id=uuid4()
    )


@events_bp.route("/<uuid:event_id>/edit", methods=["GET", "POST"], strict_slashes=False)
@login_required
def edit_event(event_id):
    event: Event | None = EventService.get_event(event_id)
    if not event:
        abort(404)

    # initialize the forms
    update_image_form = EventImageForm()

    # handle the actions
    match request.form.get("action"):
        case "update_image":
            if update_image_form.validate_on_submit():
                try:
                    is_image_updated = EventService.update_event_image(
                        event_id, update_image_form.data)
                    if is_image_updated:
                        flash("Event image updated successfully", "success")
                        return redirect(url_for("events.event_details", event_id=event_id))
                    else:
                        flash("Event image update failed", "error")
                except ValueError as e:
                    flash(e, "error")
        case _:
            pass
    return render_template(
        "events/edit_event.html",
        title="Edit Event",
        event=event,
        update_image_form=update_image_form,
        hide_footer=True,
        cache_id=uuid4()
    )


@events_bp.route("/<uuid:event_id>/save", strict_slashes=False)
@login_required
def save_event(event_id):
    is_saved = EventService.save_event(event_id, current_user.id)
    if is_saved:
        flash("Event saved successfully", "success")
        return redirect(url_for("events.event_details", event_id=event_id))
    else:
        flash("Event save failed", "error")


@events_bp.route("/<uuid:event_id>/unsave", strict_slashes=False)
@login_required
def unsave_event(event_id):
    is_unsaved = EventService.unsave_event(event_id, current_user.id)
    if is_unsaved:
        flash("Event unsaved successfully", "success")
        return redirect(url_for("events.event_details", event_id=event_id))
    else:
        flash("Event unsave failed", "error")
