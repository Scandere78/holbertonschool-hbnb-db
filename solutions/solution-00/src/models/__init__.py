"""  """
import os
from utils.constants import REPOSITORY_ENV_VAR

from src.models.base import Base
from src.models.amenity import Amenity
from src.models.db.amenity import Amenity as AmenityDB

LIST_CLASSES = {
    "Amenity": [Amenity, AmenityDB]
}

def get_class(class_name) -> Base:
    key = 0
    if os.getenv(REPOSITORY_ENV_VAR) == "db":
        key = 1
    return LIST_CLASSES.get(class_name)[key]