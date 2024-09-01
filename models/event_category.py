"""Model defines the event category"""
from sqlalchemy import Column, ForeignKey, String, Enum as SQLEnum, Text
from sqlalchemy.orm import relationship

from models.base_model import BaseModel, Base


class EventCategory(BaseModel, Base):
    """Event category model

    Defines the category
    in which the event belongs

    Attributes:
        __tablename__: The name of the table
        name: The name of the event category
        description: The description of the event category
        sub_category: The sub category of the event
    """

    __tablename__ = 'event_categories'

    name = Column(String(128), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    created_by = Column(
        String(60),
        ForeignKey('users.id'), nullable=False
    )

    # relationships
    _sub_categories = relationship(
        'EventSubCategory', back_populates='_category', lazy='select'
    )
