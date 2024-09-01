"""Module defines the ABC for the storage engine"""
from abc import ABC, abstractmethod


class StorageEngineInterface(ABC):
    """Interface for the storage engine"""

    @abstractmethod
    def all(self, cls):
        """Return all the objects"""
        pass

    @abstractmethod
    def new(self, obj):
        """Adds new object to the storage session"""
        pass

    @abstractmethod
    def save(self):
        """Commits the current session"""
        pass

    @abstractmethod
    def delete(self, obj):
        """Deletes the object"""
        pass

    @abstractmethod
    def reload(self):
        """Reloads the storage session"""
        pass

    @abstractmethod
    def close(self):
        """Closes the storage session"""
        pass

    @abstractmethod
    def get(self, cls, id):
        """Gets a specific object"""
        pass

    @abstractmethod
    def count(self, cls):
        """Gets the count of a specific modle"""
        pass
