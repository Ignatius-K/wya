"""
This module contains the service for the event model.
"""

import itertools
from datetime import datetime
import random
from flask_login import current_user

from models import storage
from models.user import User
from models.event import Event
from models.event_category import EventCategory
from models.event_sub_category import EventSubCategory
from models.enum_model import EventLocationType, EventStatus


class EventService:
    """
    This class contains the service for the event model.
    """

    @classmethod
    def get_all_events(cls, page: int = 1, per_page: int = 12):
        """
        Get all events.
        """
        events = sorted(storage.all(Event).values(),
                        key=lambda x: x.created_at, reverse=True)
        start = (page - 1) * per_page
        stop = start + per_page
        return list(itertools.islice(events, start, stop))

    @classmethod
    def get_event_categories(cls):
        """
        Get all event categories.
        """
        return sorted(storage.all(EventCategory).values(), key=lambda x: x.name)

    @classmethod
    def get_event_locations(cls):
        """
        Get all event locations.
        """
        event_locations = sorted(EventLocationType, key=lambda x: x.value)
        return event_locations

    @classmethod
    def get_event_statuses(cls):
        """
        Get all event statuses.
        """
        event_statuses = sorted(
            EventStatus, key=lambda x: x.value, reverse=True)
        return event_statuses

    @classmethod
    def get_user_events(cls, user_id: str | None = None):
        """
        Get all events for a user.
        """
        if user_id is None:
            user_id = current_user.id
        if user_id is None:
            raise ValueError("User ID is required")
        return sorted(storage.query(Event, created_by=user_id).all(), key=lambda x: x.created_at, reverse=True)

    @classmethod
    def get_event(cls, event_id: str):
        """
        Get event details.
        """
        return storage.get(Event, event_id)

    @classmethod
    def create_event(cls, data: dict):
        """
        Create an event.
        """
        event = Event(**data)

        if not event.title:
            raise ValueError("Event title is required")
        if not event.description:
            raise ValueError("Event description is required")
        if not event.start_date:
            raise ValueError("Event start date is required")
        if not event.end_date:
            raise ValueError("Event end date is required")
        if not event.location_type:
            raise ValueError("Event location type is required")
        if event.end_date < event.start_date:
            raise ValueError("Event end date must be after start date")
        if (event.end_date <= datetime.now()):
            raise ValueError("Event end date must be after current date")

        if event.start_date <= datetime.now():
            event.status = EventStatus.ON_GOING
        elif event.end_date < datetime.now():
            event.status = EventStatus.COMPLETED
        else:
            event.status = EventStatus.SCHEDULED

        event.location_type = EventLocationType.get_instance(
            data.get("location_type"))
        if event.location_type == EventLocationType.ONLINE:
            event.location_name = None
            event.location_address = None
            event.location_latitude = None
            event.location_longitude = None
        if event.location_type == EventLocationType.IN_PERSON:
            event.online_event_link = None

        # set the created by to the current user
        user_id = current_user.id
        event.created_by = user_id

        # TODO: For now, using the first sub-cateogry
        # set the category to the default category
        sub_category: EventSubCategory = random.choice(list(
            storage.all(EventSubCategory).values()))
        event.sub_category_id = sub_category.id

        try:
            print(event)
            event.save()
            return event
        except Exception as e:
            print(e)
            return None

    @classmethod
    def is_event_owner(cls, event_id: str, user_id: str):
        """
        Check if the current user is the owner of the event.
        """
        event = cls.get_event(event_id)
        return event.created_by == user_id

    @classmethod
    def is_event_saved(cls, event_id: str, user_id: str):
        """
        Check if the current user has saved the event.
        """
        user: User = storage.get(User, user_id)
        if not user:
            return False
        event = cls.get_event(event_id)
        if not event:
            return False
        for saved_event in user._events_liked:
            if saved_event == event:
                return True
        return False

    @classmethod
    def save_event(cls, event_id: str, user_id: str):
        """
        Save an event.
        """
        user: User = storage.get(User, user_id)
        if not user:
            return False
        event = cls.get_event(event_id)
        if not event:
            return False
        try:
            user._events_liked.append(event)
            user.save()
        except Exception as e:
            print(e)
            return False
        return True

    @classmethod
    def unsave_event(cls, event_id: str, user_id: str):
        """
        Unsave an event.
        """
        user: User = storage.get(User, user_id)
        if not user:
            return False
        event = cls.get_event(event_id)
        if not event:
            return False

        try:
            user._events_liked.remove(event)
            user.save()
        except Exception as e:
            print(e)
            return False
        return True

    @classmethod
    def update_event_image(cls, event_id: str, data: dict):
        """
        Update the event image.
        """
        event: Event | None = cls.get_event(event_id)
        if not event:
            return False
        try:
            event.event_image_url = data.get("image")
            event.save()
        except Exception as e:
            print(e)
            return False
        return True
