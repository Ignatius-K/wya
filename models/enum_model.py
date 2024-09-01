"""Module defines the model enums"""
from enum import Enum


class EnumModel(Enum):
    """Defines the enum model"""

    @classmethod
    def get_instance(cls, str_value):
        """Gets the enum instance"""
        for _enum in cls:
            if _enum.value == str_value or _enum.name == str_value:
                return _enum
        return None


class UserRole(EnumModel):
    """Define the user's role"""
    ADMIN = 'ADMIN'
    USER = 'USER'


class EventStatus(EnumModel):
    """Define the event status"""
    SCHEDULED = 'Scheduled'
    ON_GOING = 'Ongoing'
    CANCELLED = 'Cancelled'
    COMPLETED = 'Completed'
    POSTPONED = 'Postponed'


class EventLocationType(EnumModel):
    """Define the event location type"""
    IN_PERSON = 'In Person'
    ONLINE = 'Online'
    HYBRID = 'Hybrid'
