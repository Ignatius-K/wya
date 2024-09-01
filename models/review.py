"""Module defines the Review Model"""

from sqlalchemy import Column, ForeignKey, String, Integer, Text
from sqlalchemy.orm import relationship

from models.base_model import BaseModel, Base


class Review(BaseModel, Base):
    """Defines the review model

    User's review on the event

    Attributes:
        event_id: The event id
        user_id: The user id
        rating: The rating of the event
        comment: The comment of the event
    """

    __tablename__ = 'reviews'

    event_id = Column(String(60), ForeignKey('events.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=False)

    # relationships
    _event = relationship('Event', back_populates='_reviews', lazy='select')
    _user = relationship('User', back_populates='_reviews', lazy='select')
