"""Module defines the configuration for the application"""

from dotenv import load_dotenv
import os
from dataclasses import dataclass
import yaml


# Load environment variables
load_dotenv()

# load the yaml file
YAML_CONFIG_FILE = os.getenv("CONFIG_FILE", None)

yaml_config = {}
with open(YAML_CONFIG_FILE, "r") as file:
    try:
        yaml_config = yaml.safe_load(file)
    except Exception as e:
        print(e)

env = os.getenv("ENV", "default")
loaded_config = {**yaml_config.get("default", {}), **yaml_config.get(env, {})}


@dataclass
class Config:
    """Class defines the configuration for the application"""
    DB_USERNAME: str = os.getenv("DATABASE_USERNAME")
    DB_PASSWORD: str = os.getenv("DATABASE_PASSWORD")
    DB_HOST: str = os.getenv("DATABASE_HOST")
    DB_PORT: int = os.getenv("DATABASE_PORT")
    DB_NAME: str = os.getenv("DATABASE_NAME")

    DB_STORAGE_ENGINE: str = loaded_config.get("storage_engine")
    DB_DIALECT: str = loaded_config.get("dialect")
    DB_DRIVER: str = loaded_config.get("driver")
    DB_ENCODING: str = loaded_config.get("encoding")
    DEBUG: bool = loaded_config.get("debug")

    # Flask Config
    APP_NAME: str = loaded_config.get("app_name")
    APPLICATION_ROOT: str = loaded_config.get("application_root", "/web/")
    FLASK_HOST: str = os.getenv("FLASK_HOST")
    FLASK_PORT: int = os.getenv("WEB_FLASK_PORT")
    FLASK_DEBUG: bool = loaded_config.get("debug")
    TESTING: bool = env == "testing"
    JSONIFY_PRETTYPRINT_REGULAR: bool = loaded_config.get(
        "jsonify_prettyprint_regular", True)
    JSON_SORT_KEYS: bool = loaded_config.get("json_sort_keys", True)
    TEMPLATES_AUTO_RELOAD: bool = loaded_config.get("debug")
