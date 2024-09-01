"""Base model"""
from datetime import datetime
from uuid import uuid4
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
from enum import Enum

import models

Base = declarative_base()


class BaseModel:
    """The BaseModel class

    Defines the common attributes/methods for other models

    Attributes:
        id: The unique identifier of the model
        created_at: The date and time the model was created
        updated_at: The date and time the model was last updated
    """

    id = Column(String(60), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialize the model"""

        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)
        self.id = str(uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = self.created_at

    def __repr__(self):
        """Return the string representation of the model"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.to_dict()}"

    def to_dict(self):
        """Convert the model to a dictionary"""
        keys_to_ignore = ['_sa_instance_state', 'password', 'created_by']

        model_dict = self.__dict__.copy()
        model_dict['__class__'] = self.__class__.__name__

        # add relationship keys to ignored keys
        relationship_keys = [
            key for key in model_dict.keys() if key.startswith('_')]
        keys_to_ignore.extend(relationship_keys)

        # Remove keys
        for key in keys_to_ignore:
            model_dict.pop(key, None)

        # Replace data with values
        for key, value in model_dict.items():
            if isinstance(value, Enum):
                model_dict[key] = value.value
            if isinstance(value, datetime):
                model_dict[key] = value.isoformat()
        return model_dict

    def save(self):
        """Save the model"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def delete(self):
        """Delete the model"""
        if self is not None:
            try:
                models.storage.delete(self)
                print(f"Deleted {self}")
                print(self)
                del self
            except Exception as e:
                raise e
