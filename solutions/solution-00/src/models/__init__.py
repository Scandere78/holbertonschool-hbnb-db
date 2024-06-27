"""  """
import os
from utils.constants import REPOSITORY_ENV_VAR

from src.models.base import Base
from src.models.amenity import Amenity
from src.models.db.amenity import Amenity as AmenityDB
from src.models.city import City
from src.models.db.city import City as CityDB
from src.models.country import Country
from src.models.db.country import Country as CountryDB
from src.models.place import Place
from src.models.db.place import Place as PlaceDB
from src.models.user import User
from src.models.db.user import User as UserDB
from src.models.review import Review
from src.models.db.review import Review as ReviewDB

LIST_CLASSES = {
    "Amenity": [Amenity, AmenityDB],
    "City": [City, CityDB],
    "Country": [Country, CountryDB],
    "Place" : [Place, PlaceDB],
    "User" : [User, UserDB],
    "Review": [Review, ReviewDB]

}

def get_class(class_name) -> Base:
    key = 0
    if os.getenv(REPOSITORY_ENV_VAR) == "db":
        key = 1
    return LIST_CLASSES.get(class_name)[key]