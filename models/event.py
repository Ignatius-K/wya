"""Module defines the Event Model"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, ForeignKey, String, Integer, Table, Text, \
    Float, TIMESTAMP, Enum as SQLEnum
from sqlalchemy.orm import relationship

from models.enum_model import EventStatus, EventLocationType


# defines the table for users who liked an event
event_like_association = Table(
    "event_likes",
    Base.metadata,
    Column('event_id', String(60), ForeignKey('events.id'), primary_key=True),
    Column('user_id', String(60), ForeignKey('users.id'), primary_key=True)
)


class Event(BaseModel, Base):
    """Defines the event model"""

    __tablename__ = 'events'

    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    timezone = Column(String(50), nullable=False)
    start_date = Column(TIMESTAMP(timezone=True), nullable=False)
    end_date = Column(TIMESTAMP(timezone=True), nullable=False)
    status = Column(SQLEnum(EventStatus), default=EventStatus.SCHEDULED)

    location_type = Column(
        SQLEnum(EventLocationType), default=EventLocationType.IN_PERSON
    )
    location_name = Column(String(255))
    location_address = Column(String(255))
    location_latitude = Column(Float)
    location_longitude = Column(Float)
    google_map_link = Column(Text)
    online_event_link = Column(Text)

    event_image_url = Column(Text)
    event_website = Column(Text)

    capacity = Column(Integer)
    current_attendance = Column(Integer, default=0)

    ticket_url = Column(Text)
    tags = Column(Text)

    sub_category_id = Column(
        String(60),
        ForeignKey('event_sub_categories.id'), nullable=False
    )
    created_by = Column(
        String(60),
        ForeignKey('users.id'), nullable=False
    )

    # relationships
    _sub_category = relationship(
        'EventSubCategory', back_populates='_events', lazy='select')
    _organized_by = relationship(
        'User', back_populates='_events_organized', lazy='select')
    _liked_by = relationship(
        'User', secondary=event_like_association,
        back_populates='_events_liked', lazy='select'
    )
    _reviews = relationship(
        'Review', back_populates='_event', lazy='select')
