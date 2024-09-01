"""Model defines the sub categories of events"""

from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from models.base_model import BaseModel, Base


class EventSubCategory(BaseModel, Base):
    """Event sub category model

    Defines the sub category
    in which the event belongs
    """

    __tablename__ = 'event_sub_categories'
    name = Column(String(128), nullable=False, unique=False)
    description = Column(Text, nullable=False)
    category_id = Column(
        String(60),
        ForeignKey('event_categories.id'), nullable=False
    )
    created_by = Column(
        String(60),
        ForeignKey('users.id'), nullable=False
    )

    # relationships
    _category = relationship(
        'EventCategory', back_populates='_sub_categories', lazy='select'
    )
