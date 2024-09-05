#!/usr/bin/env python3
"""Module defines the database storage engine"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from models.user import User
from models.base_model import Base
from models.engine.storage_interface import StorageEngineInterface

from models.user import User
from models.event_category import EventCategory
from models.event_sub_category import EventSubCategory
from models.event import Event
from models.review import Review

from helpers import config


# Import all models
all_models = [
    User,
    EventCategory,
    EventSubCategory,
    Event,
    Review
]


class DBStorage(StorageEngineInterface):
    """DBStorage class

    Defines the database storage engine
    which interacts with the database

    Note:
        This depends on an ORM called SQLAlchemy

    Attributes:
        __engine: SQLAlchemy engine
        __session: SQLAlchemy session
    """

    __engine = None
    __session = None

    def __init__(self):
        """Initialize the storage engine

        The SQL engine is initiailized from
        using the provided configuration
        """
        self.__engine = create_engine(
            f"{config.DB_DIALECT}+{config.DB_DRIVER}://" +
            f"{config.DB_USERNAME}:{config.DB_PASSWORD}@" +
            f"{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}",
            client_encoding=config.DB_ENCODING,
            echo=config.SQL_ECHO,
            pool_pre_ping=True,
        )

    def reload(self):
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory=session_factory)
        self.__session = Session()

    def close(self):
        """Close the session"""
        self.__session.close()

    def all(self, cls=None):
        """Return all the objects"""
        if cls is None:
            all_objects = {}
            for model in all_models:
                all_objects.update(self.all_per_model(model))
            return all_objects
        return self.all_per_model(cls)

    def all_per_model(self, cls):
        """Get all objects per model"""
        model_objs = {}
        objs = self.__session.query(cls).all()
        for obj in objs:
            obj_key = f"{obj.__class__.__name__}.{obj.id}"
            model_objs[obj_key] = obj
        return model_objs

    def new(self, obj):
        """Adds an object to the session"""
        self.__session.add(obj)

    def save(self):
        """Commits the session"""
        try:
            self.__session.commit()
        except Exception as e:
            self.__session.rollback()
            raise e

    def delete(self, obj):
        """Deletes an object from the session"""
        if obj is not None:
            self.__session.delete(obj)
            self.save()

    def get(self, cls, id):
        """Gets a specific record from databse"""
        if cls not in all_models:
            return None
        obj_key = f'{cls.__name__}.{id}'
        return self.all_per_model(cls).get(obj_key, None)

    def query(self, model_cls, **kwargs):
        """Builds a query for a specific model"""
        if model_cls not in all_models:
            return None
        return self.__session.query(model_cls).filter_by(**kwargs)

    def count(self, cls):
        """Gets the count of a specific model"""
        if cls not in all_models:
            return 0
        return len(self.all_per_model(cls))
