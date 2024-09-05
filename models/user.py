"""User Model defines the user profile"""
from sqlalchemy import Column, String, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models.enum_model import UserRole
from models.event import event_like_association


class User(BaseModel, Base):
    """User model

    Defines the user on the system
    Note: Inherits from the BaseModel class
          For more information about the BaseModel, check out (models.base_model.BaseModel)

    Attributes:
        __tablename__: The name of the table
        first_name: The first name of the user
        last_name: The last name of the user
        email: The email of the user
        role: The role of the user
        locked: The locked status of the user
    """

    __tablename__ = 'users'

    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.USER)
    locked = Column(Boolean, nullable=False, default=False)

    # relationships
    _events_organized = relationship(
        'Event', back_populates='_organized_by', lazy='select')
    _events_liked = relationship(
        'Event', secondary=event_like_association,
        back_populates='_liked_by', lazy='select'
    )
    _reviews = relationship('Review', back_populates='_user', lazy='select')

    # flask login required methods
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return not self.locked

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id
