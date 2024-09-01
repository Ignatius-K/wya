#!/usr/bin/env python3
"""Initialize the models package"""

from enum import Enum

from models.engine.storage_interface import StorageEngineInterface

from models.engine.db_storage import DBStorage
from helpers import config


class StorageEngine(Enum):
    DB = ("db_storage", DBStorage)

    def __init__(self, engine: str, engine_class: StorageEngineInterface):
        self.engine = engine
        self.engine_class = engine_class

    @classmethod
    def get_storage_engine(cls, storage_engine: str):
        for engine in cls:
            if engine.engine.lower() == storage_engine.lower():
                return engine
        return None


if storage_engine := StorageEngine.get_storage_engine(
    config.DB_STORAGE_ENGINE
):
    storage = storage_engine.engine_class()
    storage.reload()
else:
    raise ValueError(f"Storage engine {config.DB_STORAGE_ENGINE} not found")
