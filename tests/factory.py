import uuid
from tests import PASSWORD_USER, assertStatus
from tests.client import Client


class Factory:
    client: Client

    def __init__(self, client: Client):
        self.client = client

    def create_city(self, data: dict = {}):
        """
            Helper function to create a new city.
            Sends a POST request to /cities with new city data and returns the created city's ID.
        """
        new_city = {
            "name": f"Test City {uuid.uuid4()}",
            "country_code": "UY",
            **data
        }
        response = self.client.post("/cities", new_city, self.client.superuser.access_token)
        assertStatus(response, 201)
        return response.json()["id"]


    def create_place(
        self,
        data: dict = {},
        user: dict = None,
        city_code = "UY"
    ):
        """
            Helper function to create a new place
            Sends a POST request to /places with new place data and returns the created place's ID.
        """
        host_id = self.client.user2.id
        if user:
            host_id = user['id']

        city_code = self.create_city({
            'country_code': city_code
        })
        new_place = {
            "name": f"Cozy Cottage {uuid.uuid4()}",
            "description": "A cozy cottage in the countryside.",
            "address": "123 Country Lane",
            "latitude": 34.052235,
            "longitude": -118.243683,
            "host_id": host_id,
            "city_id": city_code,
            "price_per_night": 100,
            "number_of_rooms": 2,
            "number_of_bathrooms": 1,
            "max_guests": 4,
            **data,
        }
        response = self.client.post("/places", new_place, self.client.superuser.access_token)
        assertStatus(response, 201)
        return response.json()["id"]


    def create_unique_user(self, is_admin=False):
        """
            Helper function to create a new user with a unique email
            Sends a POST request to /users with new user data and returns the created user's ID.
        """
        unique_email = f"test.user.{uuid.uuid4()}@example.com"
        new_user = {
            "email": unique_email,
            "first_name": "Test",
            "last_name": "User",
            "is_admin": is_admin,
            "password": PASSWORD_USER
        }
        response = self.client.post(f"/users", new_user)
        assertStatus(response, 201)
        return response.json()
    
    def create_unique_amenity(self, name = None):
        """
            Helper function to create a new amenity with a unique name
            Sends a POST request to /amenities with new amenity data and returns the created amenity's ID.
        """
        if not name:
            name = f"Test Amenity {uuid.uuid4()}"
        new_amenity = {"name": name}
        response = self.client.post(f"/amenities", new_amenity, self.client.superuser.access_token)
        assertStatus(response, 201)
        return response.json()["id"]
