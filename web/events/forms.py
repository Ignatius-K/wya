"""
This module defines the forms on 'events' bp
"""

from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeLocalField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError, Optional, URL

from models.enum_model import EventLocationType

from services import EventService


class StartDateValidator:
    """Validates the start date not less than today"""

    def __init__(self, message: str = "Start date must be today or later"):
        self.message = message

    def __call__(self, form, field):
        if field.data < datetime.now():
            raise ValidationError(self.message)


class EndDateValidator:
    """Validates the end date not less than start date"""

    def __init__(self, message: str = "End date must be after start date"):
        self.message = message

    def __call__(self, form, field):
        if field.data < form.start_date.data:
            raise ValidationError(self.message)


class EventForm(FlaskForm):
    """
    Define the Event Form to create an event
    """

    event_categories = EventService.get_event_categories()
    event_locations = EventService.get_event_locations()

    title = StringField(
        label="What is the name of this event? (Just give it a name 🤪)",
        render_kw={
            'placeholder': "Enter the title of the event"
        },
        validators=[DataRequired(), Length(min=5, max=255)]
    )
    description = TextAreaField(
        label="Briefly describe this event",
        render_kw={
            'placeholder': "Enter the description of the event"
        },
        validators=[DataRequired(), Length(min=5, max=255)]
    )
    category = SelectField(
        label="How would you describe your event?",
        choices=[(category.id, category.name)
                 for category in event_categories],
        validators=[DataRequired()]
    )
    timezone = StringField(
        label="Timezone",
        validators=[Optional()]
    )
    start_date = DateTimeLocalField(
        label="Start date/time",
        render_kw={
            'placeholder': "Enter the start date of the event"
        },
        validators=[DataRequired(), StartDateValidator()]
    )
    end_date = DateTimeLocalField(
        label="End date/time",
        render_kw={
            'placeholder': "Enter the end date of the event"
        },
        validators=[DataRequired(), EndDateValidator()]
    )
    location_type = SelectField(
        label="Is the event in-person, online or ...?",
        choices=[(location_type.name, location_type.value)
                 for location_type in EventLocationType],
        validators=[DataRequired()]
    )
    location_name = StringField(
        label="Where is the event taking place? (Only if event isn't online)",
        render_kw={
            'placeholder': "Enter the name of the location"
        },
        validators=[Optional(), Length(min=5, max=255)]
    )
    online_event_link = StringField(
        label="Provide the link to the event. (Only if event isn't in-person)",
        render_kw={
            'placeholder': "Enter the link to the online event"
        },
        validators=[Optional(), URL()]
    )


class EventImageForm(FlaskForm):
    """
    Define the Event Image Form to update the event image
    """

    image = StringField(
        label="Event Image",
        render_kw={
            'placeholder': "Enter the URL of the event image"
        },
        validators=[DataRequired(), URL(message="Invalid URL")]
    )
